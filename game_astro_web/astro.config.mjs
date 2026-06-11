// @ts-check
import { defineConfig } from 'astro/config';
import { webcore } from 'webcoreui/integration'

export default defineConfig({
    integrations: [webcore()]
})