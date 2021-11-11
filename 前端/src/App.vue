<template>
  <div id="app">
    <a href="https://spring.org.cn/">
      <img src="./assets/logo.png">
    </a>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.content{
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 30px;
  vertical-align: middle;
}
.main-btn{
  border-radius: 8px;
  width: 150px;
  height: 40px;
  background:rgb(111, 228, 111);
  border: 1px solid rgb(155, 154, 154);
  color:rgb(17, 17, 17);
  font-family: "微软雅黑";
  font-size: 15px;
  line-height: 50%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 10px;
  margin-right: 20px;
  margin-left: 20px;
}
.main-btn-disable{
  border-radius: 8px;
  width: 150px;
  height: 40px;
  background:rgb(133, 228, 133);
  color:rgb(126, 125, 125);
  font-family: "微软雅黑";
  font-size: 15px;
  margin-top: 10px;
  margin-right: 20px;
  margin-left: 20px;
}
.main-btn-cancel{
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0);
  width: 120px;
  height: 35px;
  background:rgb(184, 194, 184);
  color:rgb(17, 17, 17);
  font-family: "微软雅黑";
  font-size: 15px;
  line-height: 50%;
}
.main-btn-small{
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0);
  width: 120px;
  height: 35px;
  background:rgb(100, 212, 100);
  color:rgb(17, 17, 17);
  font-family: "微软雅黑";
  font-size: 15px;
  line-height: 50%;
}
.mask{
  position: fixed;
  top: 0;
  height: 100%;
  width: 100%;
  background-color: rgba(119, 119, 119, 0.644);
  opacity: 0.5;
  z-index: 8;
}
.dialog {
    border: 1.5px solid rgb(48, 48, 48);
    border-radius: 12px;
    width: 60%;
    height: 60%;
    position: absolute;
    text-align: center;
    margin: auto;
    left: 50%;
    top: 50%;
    overflow: hidden;
    transform: translate(-50%,-50%);
    background-color:white;
    z-index: 10;
}
.dialog-head{
  position: relative;
  height: 10%;
  padding-left: 3%;
  padding-top: 3%;
  font-size: 100%;
  text-align: left;
  line-height: 100%;
  background-color: #e2e2e2;
  border-bottom: 1px solid rgb(177, 176, 176);
  z-index: 1;
}
.dialog-body{
  height: 67%;
  line-height: 150%;
  font-size: 20px;
  text-align: center;
  background-color: #fff;
  overflow: auto;
}
.dialog-foot{
  border: 1px solid rgb(177, 176, 176);
  background-color: #e2e2e2;
  height: 100%;
  text-align: center;
  line-height: 52px;
}
</style>
