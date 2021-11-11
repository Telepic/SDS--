<template>
  <div class="model">
    <div class="mask"></div>
    <div class="dialog">
      <div class="dialog-head">
        <span>选择学校
        </span>
      </div>
      <div class="dialog-body">
        <div :key=school v-for = "school in schools" @click="select(school)">
          {{ school }}
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
    name: 'schools',
    mounted(){
    },
    props: ["schools"],
    data() {
        return{
            chooseschools: "",
        }
    },
    methods: {
      cancel: function () {
        this.$emit('closeschools')
      },
      select(school) {
        this.chooseschools = ""
        this.$emit('chooseschool', school)
      }
    },
    mounted() {
      this.chooseschools=this.schools;
    }
}
</script>
