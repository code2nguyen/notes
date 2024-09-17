// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'My Notes',
			social: {
				github: 'https://github.com/code2nguyen/notes',
			},
			sidebar: [
				{
					label: 'AWS',
					autogenerate: { directory: 'aws' },

				}
			],
		}),
	],
});
