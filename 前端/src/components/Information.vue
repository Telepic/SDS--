<template>
<div class='info'>
    <h1>{{ title }}</h1>
    <div class="content">
      <button class="main-btn" @click="chooseSchools">{{ school }}</button>
      <button class="main-btn" @click="chooseStudents" :disabled="school=='选择学校'">{{ student }}</button>
      <div v-if="student!='选择学生'">
        <h2>
          <button class="main-btn" @click='info'>查看抽签信息</button>
        </h2>
      </div>
      <div v-else>
        <h2>
          <button class="main-btn-disable" :disabled="student=='选择学生'">查看抽签信息</button>
        </h2>
      </div>
      <div v-if="showschool==true">
        <Schools :schools="schools" @closeschools='showschools' @chooseschool='chooseSchool'>
        </Schools>
      </div>
      <div v-if="showstudent==true">
        <Students :students="students" @closestudents='showstudents' @choosestudent='chooseStudent'>
        </Students>
      </div>
      <div v-if="showresult==true">
        <Result :results="result" @closeresult='showresult_close' @print='print'>
        </Result>
      </div>
    </div>
    <button class="main-btn" @click='back'>返回</button>
</div>
</template>

<script>
import Schools from '@/components/Schools';
import Students from '@/components/Students';
import Result from '@/components/Result'

export default {
    name: "information",
    data() {
        return{
            title: "查询-补充打印界面",
            school: "选择学校",
            student: "选择学生",
            showschool: false,
            showstudent: false,
            showresult: false,
            schools: [],
            students: [],
            result: {},
        }
    },
    components:{
      Result,
      Students,
      Schools
    },
    methods:{
        back(){
            this.$router.replace('/')
        },
        showschools(){
          this.showschool = false;
        },
        showstudents(){
          this.showstudent = false;
        },
        showresult_close(){
          this.showresult = false;
        },
        chooseSchools() {
          this.school = '选择学校';
          this.student = '选择学生';
          this.showschool = true;
          this.$axios.get('/get_drawn_schools').then(res =>
            this.schools = res.data).catch(error =>
            console.error(error))
        },
        chooseStudents() {
          this.student = '选择学生';
          this.showstudent = true;
          this.$axios.get(`/get_drawn_students/${this.school}`).then(res =>
            this.students = res.data).catch(error =>
            console.error(error))
        },
        chooseStudent(student) {
          this.student = student;
          this.showstudent = false
        },
        chooseSchool(school) {
          this.school = school;
          this.showschool = false;
        },
        info(){
            this.$axios.get(`/get_result/${this.school}/${this.student}`).then(res =>
            this.result = res.data).catch(error =>
            console.error(error));
            this.showresult = true;
        },
        print() {
          this.$axios.get(`/print_result/${this.school}/${this.student}`).then(res =>
            this.printsucc = true,
            alert("打印请求发送成功！")
            ).catch(error =>
            console.error(error))
          this.showresult = false;
          this.school = '选择学校';
          this.student = '选择学生';
        }
    },
}
</script>

<style scoped>
h1{
  font-weight: normal;
}
h2{
  font-weight: normal;
  font-size: 15px;
  line-height: 150%;
}
</style>