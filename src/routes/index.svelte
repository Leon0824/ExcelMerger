<script>
  import { browser } from "$app/env";
  import { open, save } from "../../node_modules/@tauri-apps/api/dialog";
  import { Command } from "../../node_modules/@tauri-apps/api/shell";
  import { listen } from "../../node_modules/@tauri-apps/api/event";
  import XLSX from "xlsx-js-style";
  import iconv from "iconv-lite";

  if (browser) {
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
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
      ]);

      // for (const file of files) {
      //   if (!fileType.has(file.type)) {
      //     setBackgroundNormal();
      //     alert(`${file.name} 非 Excel 檔案`);
      //     return false;
      //   }
      // }

      const command = Command.sidecar("merger", files);
      const output = await command.execute();
      console.log(output);

      // for (const file of files) {
      //   const reader = new FileReader();
      //   reader.readAsArrayBuffer(file);
      //   reader.onload = (e) => {
      //     const data = new Uint8Array(e.target.result);
      //     const workbook = XLSX.read(data, { type: "array" });

      //     /* DO SOMETHING WITH workbook HERE */
      //     console.log(workbook);
      //     const firstSheetName = workbook.SheetNames[0];
      //     const firstSheet = workbook.Sheets[firstSheetName];

      //     Object.entries(firstSheet).forEach(([key, value]) => {
      //       if (value.v) value.v = iconv.decode(value.v, "big5");
      //     });

      //     /* output format determined by filename */
      //     XLSX.writeFile(workbook, "out.xlsx");
      //     /* at this point, out.xlsx will have been downloaded */
      //   };
      // }

      setBackgroundNormal();
    }

    async function click(e) {
      const files = await open({
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
  <!-- <script src="https://unpkg.com/xlsx/dist/xlsx.full.min.js"></script> -->
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
