<template>
<TitleBar/>
<select name="detect-mode" v-model="detectModeSelected">
    <option v-for="(modeItem, ix) in detectModeList" v-bind:value="modeItem.mode" v-bind:key="ix">{{ modeItem.text }}</option>
</select>    
<button v-on:click="loadVideoPy">動画ファイルを読み込む</button>
</template>

<script>
import TitleBar from './components/TitleBar.vue'

const DETECT_MODE = {
    VOLUME: 'VOLUME',
    WAVEFORM: 'WAVEFORM'
}

export default {
    name: 'App',
    data() {
        return {
            detectModeSelected: DETECT_MODE.WAVEFORM,
            detectModeList: [
                { text: '波形モード(推奨)', mode: DETECT_MODE.WAVEFORM },
                { text: '音量モード', mode: DETECT_MODE.VOLUME }
            ]
        }
    },
    methods: {
        loadVideoPy() {
            window.pywebview.api.load_video(this.detectModeSelected);
        }
    },
    components: {
        TitleBar
    }
}
</script>