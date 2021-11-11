<template>
  <div class="draw_index">
    <h1>{{ msg }}</h1>
    <ul>
      <li>
        <button class="main-btn" @click="drawIn">抽签</button>
      </li>
      <li>
        <button class="main-btn" @click="info">查看抽签信息</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Index',
  data() {
    return {
      msg: '春禾-小组抽签系统'
    }
  },
  methods: {
    drawIn(){
      this.$router.replace('/choose')
    },
    info(){
      this.$router.replace('/info')
    }
  }
}
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  height: 60px;
  margin: 0 10px;
}
</style>
