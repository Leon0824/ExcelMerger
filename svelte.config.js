import adapter from '@sveltejs/adapter-static';
import { isoImport } from 'vite-plugin-iso-import';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter( {
			// default options are shown. On some platforms
			// these options are set automatically — see below
			pages: 'build',
			assets: 'build',
			fallback: 'index.html',
			precompress: false,
		} ),

		prerender: {
			// This can be false if you're using a fallback (i.e. SPA mode)
			default: false,
		},
	},
};

export default config;
