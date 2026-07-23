/** @type {import("stylelint").Config} */
export default {
	extends: ['stylelint-config-standard'],
	overrides: [
		{
			files: ['**/*.astro'],
			extends: ['stylelint-config-html/astro'],
		},
	],

	rules: {
		'declaration-no-important': true,
		'comment-empty-line-before': null,
		'declaration-empty-line-before': null,
		'custom-property-empty-line-before': null,
	},
};
