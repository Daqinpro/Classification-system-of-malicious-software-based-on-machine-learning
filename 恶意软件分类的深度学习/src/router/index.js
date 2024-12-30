import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const router = new Router({
  mode: 'history', // 启用 history 模式
  routes: [
    {
      path: '/',
      name: 'login',
      component: ()=> import('@/components/login')
    },
    {
      path: '/home',
      name: 'home',
      component: ()=> import('@/components/home'),
      redirect: '/sampleSnalysis',
      children: [
        {
          path:'/sampleSnalysis',
          name: 'sampleSnalysis',
          component: ()=> import('@/components/sampleSnalysis/sampleSnalysis')
        },
        {
          path:'/historicalQueries',
          name: 'historicalQueries',
          component: ()=> import('@/components/historicalQueries/historicalQueries')
        },
        {
          path:'/accountManagement',
          name: 'accountManagement',
          component: ()=> import('@/components/accountManagement/accountManagement')
        },
        {
          path:'/userManagement',
          name: 'userManagement',
          component: ()=> import('@/components/userManagement/userManagement')
        },{
          path:'/menuManagement',
          name: 'menuManagement',
          component: ()=> import('@/components/menuManagement/menuManagement')
        },{
          path:'/homePage',
          name: 'homePage',
          component: ()=> import('@/components/homePage/homePage')
        }

      ]


    }
  ]
})

const routerPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return routerPush.call(this, location).catch(error => error)
}

router.beforeEach((to, from, next) => {
  if (to.path == "/") {
    next()
  } else {
    let token = window.sessionStorage.getItem("token")
    if (!token) {
      next('/')
    } else {
      next()
    }
  }
})

export default router
