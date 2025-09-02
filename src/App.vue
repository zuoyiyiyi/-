<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <a class="navbar-brand" href="#">情感感知打卡机器人</a>
        <div class="navbar-nav ml-auto">
          <span v-if="authenticated" class="navbar-text">
            欢迎，{{ logged_user_name }}！
          </span>
          <button v-if="authenticated" @click="logout" class="btn btn-outline-light ml-2">
            退出
          </button>
        </div>
      </div>
    </nav>

    <div class="main-content">
      <!-- 登录页面 -->
      <div v-if="!authenticated" class="container mt-5">
        <div class="row justify-content-center">
          <div class="col-md-6">
            <Login @login-success="setAuthenticated" />
          </div>
        </div>
      </div>

      <!-- 主应用内容 -->
      <div v-else class="container-fluid">
        <div class="row">
          <!-- 侧边栏 -->
          <div class="col-md-3 col-lg-2 sidebar">
            <div class="list-group">
              <a 
                href="#" 
                @click.prevent="currentView = 'chat'"
                :class="['list-group-item', 'list-group-item-action', currentView === 'chat' ? 'active' : '']"
              >
                <i class="fas fa-comments mr-2"></i>
                聊天
              </a>
              <a 
                href="#" 
                @click.prevent="currentView = 'goals'"
                :class="['list-group-item', 'list-group-item-action', currentView === 'goals' ? 'active' : '']"
              >
                <i class="fas fa-bullseye mr-2"></i>
                目标管理
              </a>
              <a 
                href="#" 
                @click.prevent="currentView = 'checkin'"
                :class="['list-group-item', 'list-group-item-action', currentView === 'checkin' ? 'active' : '']"
              >
                <i class="fas fa-calendar-check mr-2"></i>
                打卡管理
              </a>
            </div>
          </div>

          <!-- 主内容区域 -->
          <div class="col-md-9 col-lg-10 main-content-area">
            <!-- 聊天界面 -->
            <div v-if="currentView === 'chat'">
              <div class="row">
                <div class="col-md-4">
                  <UserList 
                    :users="users" 
                    :current-user-id="logged_user_id"
                    @select-user="selectUser"
                  />
                </div>
                <div class="col-md-8">
                  <ChatWindow 
                    v-if="selectedUser && currentChannel"
                    :current-user-id="logged_user_id"
                    :selected-user="selectedUser"
                    :channel="currentChannel"
                  />
                  <div v-else class="text-center py-5">
                    <i class="fas fa-comments fa-3x text-muted mb-3"></i>
                    <p class="text-muted">选择一个用户开始聊天</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 目标管理 -->
            <div v-else-if="currentView === 'goals'">
              <GoalManager ref="goalManager" :user-id="logged_user_id" />
            </div>

            <!-- 打卡管理 -->
            <div v-else-if="currentView === 'checkin'">
              <CheckInManager :user-id="logged_user_id" @refresh-goal-reminders="refreshGoalReminders" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast 通知 -->
    <b-toast id="toast" />
  </div>
</template>

<script>
import Login from './components/Login.vue'
import UserList from './components/UserList.vue'
import ChatWindow from './components/ChatWindow.vue'
import GoalManager from './components/GoalManager.vue'
import CheckInManager from './components/CheckInManager.vue'

export default {
  name: 'App',
  components: {
    Login,
    UserList,
    ChatWindow,
    GoalManager,
    CheckInManager
  },
  data() {
    return {
      authenticated: false,
      logged_user_id: null,
      logged_user_name: '',
      users: [],
      selectedUser: null,
      currentChannel: null,
      currentView: 'chat'
    }
  },
  mounted() {
    // 检查是否已登录
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      const user = JSON.parse(savedUser)
      this.setAuthenticated(user)
    }
  },
  methods: {
    setAuthenticated(user) {
      this.authenticated = true
      this.logged_user_id = Number(user.id)
      console.log('当前登录用户ID:', this.logged_user_id, typeof this.logged_user_id)
      this.logged_user_name = user.username
      localStorage.setItem('user', JSON.stringify(user))
      this.loadUsers()
    },
    
    logout() {
      this.authenticated = false
      this.logged_user_id = null
      this.logged_user_name = ''
      this.users = []
      this.selectedUser = null
      this.currentChannel = null
      this.currentView = 'chat'
      localStorage.removeItem('user')
    },
    
    async loadUsers() {
      try {
        const response = await this.$axios.get('/users/')
        console.log('所有用户:', response.data)
        console.log('当前ID:', this.logged_user_id, typeof this.logged_user_id)
        this.users = response.data.filter(user => user.id !== this.logged_user_id)
        console.log('过滤后用户:', this.users)
      } catch (error) {
        console.error('加载用户列表失败:', error)
      }
    },
    
    async selectUser(user) {
      this.selectedUser = user
      try {
        const response = await this.$axios.post('/request_chat', {
          from_user: this.logged_user_id,
          to_user: user.id
        })
        this.currentChannel = {
          id: response.data.channel_id,
          name: response.data.channel_name
        }
      } catch (error) {
        console.error('创建聊天频道失败:', error)
      }
    },
    
    refreshGoalReminders() {
      // 调用GoalManager的刷新方法
      if (this.$refs.goalManager) {
        this.$refs.goalManager.refreshReminders()
      }
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.navbar {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.main-content {
  min-height: calc(100vh - 56px);
}

.sidebar {
  background-color: white;
  min-height: calc(100vh - 56px);
  padding: 20px 0;
  box-shadow: 2px 0 4px rgba(0,0,0,0.1);
}

.main-content-area {
  padding: 20px;
}

.list-group-item {
  border: none;
  border-radius: 0;
  padding: 12px 20px;
}

.list-group-item.active {
  background-color: #007bff;
  border-color: #007bff;
}

.list-group-item:hover {
  background-color: #f8f9fa;
}

.list-group-item.active:hover {
  background-color: #0056b3;
}

.fas {
  width: 16px;
}
</style>
