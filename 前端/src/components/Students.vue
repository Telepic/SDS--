<template>
  <div class="model">
    <div class="mask"></div>
    <div class="dialog">
      <div class="dialog-head">
        <span>选择学生
        </span>
      </div>
      <div class="dialog-body">
        <div :key=student v-for = "student in students" @click="select(student)">
          {{ student }}
        </div>
      </div>
      <div class="dialog-foot">
        <button class="main-btn-cancel" @click="cancel">取消</button>
      </div>
    </div>
  </div>
</template>

<script>
export default{
    name: 'students',
    mounted(){
    },
    props: ["students"],
    data() {
        return{
            choosestudents: "",
        }
    },
    methods: {
      cancel: function () {
        this.$emit('closestudents')
      },
      select(student) {
        this.$emit('choosestudent', student)
      }
    },
    mounted() {
      this.choosestudents=this.students;
    }
}
</script>
