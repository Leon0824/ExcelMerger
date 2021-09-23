<script>
  import { browser } from "$app/env";
  import { open, save } from "../../node_modules/@tauri-apps/api/dialog";
  import { Command } from "../../node_modules/@tauri-apps/api/shell";
  import { listen } from "../../node_modules/@tauri-apps/api/event";
  import { copyFile } from "../../node_modules/@tauri-apps/api/fs";
  // import { dirname } from "../../node_modules/@tauri-apps/api/path";

  if (browser) {
    document.oncontextmenu = () => {
      // return false;
    };

    const dropbox = document.getElementById("dropbox");

    function setBackgroundNormal() {
      dropbox.classList.add("normal");
      dropbox.classList.remove("dragenter");
    }

    function setBackgroundDragenter() {
      dropbox.classList.add("dragenter");
      dropbox.classList.remove("normal");
    }

    async function handleFiles(files) {
      const fileType = new Set([
        "xlsx",
        "xls",
      ]);

      for (const file of files) {
        const fileExt = file.split('.').slice(-1)[0].toLowerCase();
        if (!fileType.has(fileExt)) {
          alert(`${file} 非 Excel 檔案`);
          return false;
        }
      }

      const command = Command.sidecar("merger", files);
      const output = await command.execute();

      if (output.code === 0) {
        const mergedFileTempPath = output.stdout;
        const mergedFileName = mergedFileTempPath.split('\\').pop();
        const defaultSavePath = files[0].split("\\").slice(0, -1).join('\\') + '\\' + mergedFileName;
        const savePath = await save({
          defaultPath: defaultSavePath,
        });

        await copyFile(mergedFileTempPath, savePath);
      }
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
        handleFiles(files);
      }
    }

    function drop(e) {
      e.stopPropagation();
      e.preventDefault();
      const files = e.dataTransfer.files;
      handleFiles(files);
    }

    dropbox.addEventListener("drop", drop, false);
    dropbox.addEventListener("click", click, false);

    listen("tauri://file-drop-hover", (e) => {
      setBackgroundDragenter();
    });

    listen("tauri://file-drop-cancelled", (e) => {
      setBackgroundNormal();
    });

    listen("tauri://file-drop", (e) => {
      const files = e.payload
      handleFiles(files);
      setBackgroundNormal();
    });
  }
</script>

<svelte:head>
</svelte:head>

<div
  id="dropbox-container"
  class="grid grid-cols-1 grid-rows-1 h-screen place-items-center bg-blue-50"
>
  <div
    class="place-self-center w-full h-full row-span-full col-span-full z-10 bg-center bg-no-repeat h-screen p-16 bg-blue-50 hover:bg-blue-100 bg-contain cursor-pointer normal"
    id="dropbox"
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
</style>
