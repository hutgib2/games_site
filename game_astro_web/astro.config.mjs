// @ts-check
import { defineConfig, fontProviders } from 'astro/config';
import { webcore } from 'webcoreui/integration'

export default defineConfig({
    integrations: [webcore()],
    fonts: [
		{
			provider: fontProviders.local(),
			name: 'Oswald',
			cssVariable: '--font-oswald',
            optimizedFallbacks: false,
			options: {
				variants: [
					{
						src: ['./src/assets/fonts/Oswald-Light.ttf'],
						style: 'normal',
						weight: 300,
					},
					{
						src: ['./src/assets/fonts/Oswald-Regular.ttf'],
						style: 'normal',
						weight: 400,
					},
					{
						src: ['./src/assets/fonts/Oswald-Medium.ttf'],
						style: 'normal',
						weight: 500,
					},
				],
			},
		},
	],
})