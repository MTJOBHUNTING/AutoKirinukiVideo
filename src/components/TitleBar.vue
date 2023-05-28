<template>
<div>
    <TitleBarButton hoverColor="var(--hover-color)" icon="window-minimize" v-on:click="minimizeWindow"/>
    <TitleBarButton hoverColor="var(--warning-color)" icon="close" v-on:click="closeWindow"/>
</div>
</template>

<script>
import TitleBarButton from './TitleBarButton.vue';
export default {
    name: 'TitleBar',
    methods: {
        minimizeWindow() {
            window.pywebview.api.minimize_window();
        },
        closeWindow() {
            window.pywebview.api.close_window();
        }
    },
    components: {
        TitleBarButton
    }
}
</script>


<style scoped lang="scss">
@use '@/themes/default.scss' as themes;
@use '@/styles/settings.scss' as settings;
div {
    display: flex;
    justify-content: flex-end;
    width: settings.$titlebar-width;
    height: settings.$titlebar-height;
    background-color: var(--primary-color);

    border-bottom: settings.$border-line-width solid var(--border-line-color)
}
</style>