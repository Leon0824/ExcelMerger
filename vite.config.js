import { defineConfig } from 'vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import { isoImport } from 'vite-plugin-iso-import';

/** @type {import('vite').UserConfig} */
const config = {
    plugins: [
        sveltekit(),
        isoImport(),
    ]
};

export default config;
