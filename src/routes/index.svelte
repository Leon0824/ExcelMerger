<script>
  import { browser } from "$app/env";
  import { onMount } from "svelte";
  import { open, save } from "@tauri-apps/api/dialog?client";
  import { Command } from "@tauri-apps/api/shell?client";
  import { listen } from "@tauri-apps/api/event?client";
  import { copyFile } from "@tauri-apps/api/fs?client";

  function setBackgroundNormal() {
    dropbox.classList.add("normal");
    dropbox.classList.remove("dragenter");
    dropbox.classList.remove("processing");
  }

  function setBackgroundDragenter() {
    dropbox.classList.add("dragenter");
    dropbox.classList.remove("normal");
  }

  function setBackgroundProcessing() {
    dropbox.classList.add("processing");
    dropbox.classList.remove("dragenter");
    dropbox.classList.remove("normal");
  }

  async function handleFiles(files) {
    const fileType = new Set(["xlsx", "xls"]);

    for (const file of files) {
      const fileExt = file.split(".").slice(-1)[0].toLowerCase();
      if (!fileType.has(fileExt)) {
        alert(`${file} 非 Excel 檔案`);
        setBackgroundNormal();
        return false;
      }
    }

    const command = Command.sidecar("../src-python/dist/merger", files);
    const output = await command.execute();

    if (output.code === 0) {
      let mergedFileTempPath = output.stdout;
      mergedFileTempPath = mergedFileTempPath.trimEnd();
      const mergedFileName = mergedFileTempPath.split("\\").pop();
      let defaultSavePath =
        files[0].split("\\").slice(0, -1).join("\\") + "\\" + mergedFileName;
      defaultSavePath = defaultSavePath.trimEnd();
      const savePath = await save({
        defaultPath: defaultSavePath,
      });

      if (savePath) {
        await copyFile(mergedFileTempPath, savePath);
      }
    } else {
      console.error(output.stderr);
      alert(output.stderr);
    }

    setBackgroundNormal();
  }

  function drop() {
    // e.stopPropagation();
    // e.preventDefault();
    const files = e.dataTransfer.files;
    handleFiles(files);
  }

  async function click(e) {
    let files = await open({
      directory: false,
      // filters: {
      //   name: "*",
      //   extensions: ["xlsx", "xls"],
      // },
      multiple: true,
    });

    if (typeof files === "string") {
      files = [files];
    }

    if (files !== null) {
      setBackgroundProcessing();
      handleFiles(files);
    }
  }

  onMount(() => {
    listen("tauri://file-drop-hover", (e) => {
      console.log(e);
      setBackgroundDragenter();
    });

    listen("tauri://file-drop-cancelled", (e) => {
      setBackgroundNormal();
    });

    listen("tauri://file-drop", (e) => {
      setBackgroundProcessing();
      const files = e.payload;
      handleFiles(files);
    });
  });

  if (browser) {
    document.oncontextmenu = () => {
      return false;
    };

    const dropbox = document.getElementById("dropbox");
  }
</script>

<svelte:head />

<div
  id="dropbox-container"
  class="grid grid-cols-1 grid-rows-1 h-screen place-items-center bg-blue-50"
>
  <div
    class="place-self-center w-full h-full row-span-full col-span-full z-10 bg-center bg-no-repeat h-screen p-16 bg-blue-50 hover:bg-blue-100 bg-contain cursor-pointer normal"
    id="dropbox"
    on:drop={drop}
    on:click={click}
  />

  <div class="row-span-full col-span-full text-center">
    <input type="file" id="file-input" accept=".xlsx, .xls" multiple />
  </div>
</div>

<style>
  #dropbox-container {
    user-select: none;
  }

  #dropbox {
    max-width: 400px;
    max-height: 400px;
    aspect-ratio: 1;
  }
  .normal {
    background-image: url("/normal.svg");
  }

  :global(.dragenter) {
    background-image: url("/dragenter.svg");
  }

  :global(.processing) {
    background-image: url("/processing.svg");
  }
</style>
