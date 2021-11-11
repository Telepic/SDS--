<template>
  <div class='choose'>
    <h1>{{ title }}</h1>
    <div class="content">
      <button class="main-btn" @click="chooseSchools">{{ school }}</button>
      <button class="main-btn" @click="chooseStudents" :disabled="school=='选择学校'">{{ student }}</button>
      <div v-if="student!='选择学生'">
        <h2>
          <button class="main-btn" @click='draw'>抽签</button>
        </h2>
      </div>
      <div v-else>
        <h2>
          <button class="main-btn-disable" :disabled="student=='选择学生'">抽签</button>
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
    name: 'Draw',
    data () {
        return{
            title: '抽签界面',
            school: '选择学校',
            student: '选择学生',
            schools: [],
            students: [],
            showschool: false,
            showstudent: false,
            showresult: false,
            printinfo: false,
            printsucc: false,
            result: {},
            isDraw: false,
        }
    },
    components:{
      Result,
      Students,
      Schools
    },
    methods: {
        back(){
          this.$router.replace('/')
        },
        chooseSchools() {
          this.school = '选择学校';
          this.student = '选择学生';
          this.showschool = true;
          this.$axios.get('/getSchools').then(res =>
            this.schools = res.data).catch(error =>
            console.error(error))
        },
        showschools(){
          this.showschool = false;
        },
        showstudents(){
          this.showstudent = false;
        },
        showresult_close(){
          this.showresult = false;
          this.school = '选择学校';
          this.student = '选择学生';
        },
        chooseSchool(school) {
          this.school = school;
          this.showschool = false;
        },
        chooseStudents() {
          this.student = '选择学生';
          this.showstudent = true;
          this.$axios.get(`/getStudents/${this.school}`).then(res =>
            this.students = res.data).catch(error =>
            console.error(error))
        },
        chooseStudent(student) {
          this.student = student;
          this.showstudent = false
        },
        draw() {
          this.$axios.get(`/draw/${this.school}/${this.student}`).then(res =>
            this.result = res.data).catch(error =>
            console.error(error));
          for(var key in this.result){
            if(this.result[key]=="isDraw"&&key=="false"){ // 似乎有些问题
              this.isDraw = true;
              break;
            }
          }
          if(this.isDraw){ 
            // 提示已抽签,未写
          }else{
            this.showresult = true
          }
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