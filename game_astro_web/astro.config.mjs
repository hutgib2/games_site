// @ts-check
import { defineConfig, fontProviders } from 'astro/config';
import { webcore } from 'webcoreui/integration'

export default defineConfig({
    integrations: [webcore()],
    fonts: [
		{
			name: 'Oswald',
			provider: fontProviders.google(),
			cssVariable: '--font-oswald',
            weights: [300, 400, 500, 600],
			styles: ["normal"],
		},
	],
})