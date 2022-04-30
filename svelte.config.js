import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			// default options are shown
			pages: 'build',
			assets: 'build',
			fallback: 'index.html',
		}),
		// hydrate the <div id="svelte"> element in src/app.html
		// target: '#svelte',
	},
};

export default config;
