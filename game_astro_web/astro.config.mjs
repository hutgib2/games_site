// @ts-check
import cloudflare from '@astrojs/cloudflare';
import { webcore } from 'webcoreui/integration'
import { defineConfig, fontProviders } from 'astro/config';

export default defineConfig({
	adapter: cloudflare(),
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
