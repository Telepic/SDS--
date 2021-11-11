import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Choose from '@/components/Choose'
import Information from '@/components/Information'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/choose',
      name: 'Choose',
      component: Choose
    },
    {
      path: '/info',
      name: 'Information',
      component: Information
    }
  ],
  mode: 'history',
})
