// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://code2nguyen.github.io/',
	base: 'notes',
	integrations: [
		starlight({
			title: 'My Notes',
			social: {
				github: 'https://github.com/code2nguyen/notes',
			},
			customCss: [
				// Relative path to your custom CSS file
				'./src/styles/custom.css',
			],
			sidebar: [
				{
					label: 'AWS',
					autogenerate: { directory: 'aws' },

				},
				{
					label: 'Machine Learning',
					autogenerate: { directory: 'ml' },

				},
				{
					label: 'Python',
					autogenerate: { directory: 'python' },

				},
				{
					label: 'DevOps',
					autogenerate: { directory: 'devops' },

				},
				{
					label: 'Miscellaneous',
					autogenerate: { directory: 'others' },

				}
			],
		}),
	],
});
