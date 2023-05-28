<template>
<div class="button">
    <fa v-bind:icon="icon"/>
</div>
</template>

<script>
export default {
    name: 'TitleBarButton',
    props: {
        hoverColor: {
            type: String
        },
        icon: {
            type: String
        }
    }
}
</script>


<style scoped lang="scss">
@use '@/themes/default.scss' as themes;
@use '@/styles/settings.scss' as settings;

.button {
    align-items: center;
    justify-content: center;
    width: settings.$titlebar-button-width;
    height: settings.$titlebar-button-height;
    transition: background-color .25s;
    color: var(--text-color);
    font-size: settings.$titlebar-button-height;
    &:hover {
        background-color: v-bind(hoverColor);
    }
}
</style>