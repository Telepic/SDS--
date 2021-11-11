<template>
    <div class="model">
    <div class="mask"></div>
    <div class="dialog">
      <div class="dialog-head">
        <span>抽签结果
        </span>
      </div>
      <div class="dialog-body">
        <div class="result-dialog-body">
          <div :key=result v-for = "(key,result) in results"><span v-if="result=='name'">姓名:{{ key }}</span></div>
          <div :key=result v-for = "(key,result) in results"><span v-if="result=='school'">学校:{{ key }}</span></div>
          <div :key=result v-for = "(key,result) in results"><span v-if="result=='zone'">赛区:{{ key }}</span></div>
          <div :key=result v-for = "(key,result) in results"><span v-if="result=='group'">小组号:{{ key }}</span></div>
        </div>
      </div>
      <div class="dialog-foot">
        <button class="main-btn-small" @click="print">打印</button>
        <button class="main-btn-cancel" @click="cancel">取消</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name: "result",
    props: ["results"],
    methods: {
      cancel() {
        this.$emit('closeresult')
      },
      print(){
        this.$emit('print')
      }
    },
    
}
</script>

<style>
.result-dialog-body{
  height: 100%;
  line-height: 200%;
  font-size: 20px;
  text-align: left;
  margin: 5%;
  text-indent: 5%;
  background-color: #fff;
  overflow: auto;
}
</style>