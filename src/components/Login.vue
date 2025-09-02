<template>
  <div class="login-container">
    <div class="card">
      <div class="card-header text-center">
        <h3>情感感知打卡机器人</h3>
        <p class="text-muted">登录或注册开始使用</p>
      </div>
      <div class="card-body">
        <!-- 标签页导航 -->
        <div class="nav nav-tabs mb-3">
          <button 
            class="nav-link btn btn-link" 
            :class="{ active: currentTab === 'login' }"
            @click="currentTab = 'login'"
          >
            登录
          </button>
          <button 
            class="nav-link btn btn-link" 
            :class="{ active: currentTab === 'register' }"
            @click="currentTab = 'register'"
          >
            注册
          </button>
        </div>
        
        <!-- 登录表单 -->
        <div v-if="currentTab === 'login'">
          <form @submit.prevent="login">
            <div class="form-group">
              <label>用户名</label>
              <input 
                v-model="loginForm.username" 
                type="text" 
                class="form-control" 
                placeholder="请输入用户名"
                required
              >
            </div>
            <div class="form-group">
              <label>密码</label>
              <input 
                v-model="loginForm.password" 
                type="password" 
                class="form-control" 
                placeholder="请输入密码"
                required
              >
            </div>
            <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
              {{ loading ? '登录中...' : '登录' }}
            </button>
          </form>
        </div>
        
        <!-- 注册表单 -->
        <div v-if="currentTab === 'register'">
          <form @submit.prevent="register">
            <div class="form-group">
              <label>用户名</label>
              <input 
                v-model="registerForm.username" 
                type="text" 
                class="form-control" 
                placeholder="请输入用户名"
                required
              >
            </div>
            <div class="form-group">
              <label>密码</label>
              <input 
                v-model="registerForm.password" 
                type="password" 
                class="form-control" 
                placeholder="请输入密码"
                required
              >
            </div>
            <div class="form-group">
              <label>确认密码</label>
              <input 
                v-model="registerForm.confirmPassword" 
                type="password" 
                class="form-control" 
                placeholder="请再次输入密码"
                required
              >
            </div>
            <button type="submit" class="btn btn-success btn-block" :disabled="loading">
              {{ loading ? '注册中...' : '注册' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      currentTab: 'login',
      loading: false,
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        confirmPassword: ''
      }
    }
  },
  methods: {
    async login() {
      if (!this.loginForm.username || !this.loginForm.password) {
        alert('请填写完整的登录信息')
        return
      }
      
      this.loading = true
      try {
        console.log('开始登录请求...')
        
        // 使用this.$axios替代fetch
        const response = await this.$axios.post('login/', {
          username: this.loginForm.username,
          password: this.loginForm.password
        })
        const data = response.data
        
        console.log('登录成功，响应数据:', data)
        this.$emit('login-success', data)
        alert('登录成功')
      } catch (error) {
        console.error('登录失败详细信息:', error)
        let errorMsg = '登录失败，请重试'
        if (error.response && error.response.data && error.response.data.error) {
          errorMsg = error.response.data.error
        } else if (error.message.includes('Failed to fetch')) {
          errorMsg = '网络连接失败，请检查网络'
        } else {
          errorMsg = error.message || '未知错误'
        }
        alert(`登录失败: ${errorMsg}`)
      } finally {
        this.loading = false
      }
    },
    
    async register() {
      if (!this.registerForm.username || !this.registerForm.password || !this.registerForm.confirmPassword) {
        alert('请填写完整的注册信息')
        return
      }
      
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        alert('两次输入的密码不一致')
        return
      }
      
      this.loading = true
      try {
        console.log('开始注册请求...')
        console.log('请求数据:', {
          username: this.registerForm.username,
          password: this.registerForm.password
        })
        // 使用this.$axios替代fetch
        const response = await this.$axios.post('register/', {
          username: this.registerForm.username,
          password: this.registerForm.password
        })
        const data = response.data
        
        console.log('注册成功，响应数据:', data)
        // 注册成功后自动登录
        this.$emit('login-success', data)
        alert('注册成功，已自动登录')
      } catch (error) {
        console.error('注册失败详细信息:', error)
        let errorMsg = '注册失败，请重试'
        if (error.response && error.response.data && error.response.data.error) {
          errorMsg = error.response.data.error
        } else if (error.message.includes('Failed to fetch')) {
          errorMsg = '网络连接失败，请检查网络'
        } else {
          errorMsg = error.message || '未知错误'
        }
        alert(`注册失败: ${errorMsg}`)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
}

.card {
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 15px 15px 0 0 !important;
  border: none;
}

.nav-tabs {
  border-bottom: 1px solid #dee2e6;
}

.nav-tabs .btn-link {
  border: none;
  color: #6c757d;
  text-decoration: none;
}

.nav-tabs .btn-link.active {
  color: #007bff;
  background-color: transparent;
  border-bottom: 2px solid #007bff;
}

.form-group {
  margin-bottom: 1rem;
}

.form-control {
  border-radius: 8px;
  border: 1px solid #ddd;
  padding: 10px 15px;
}

.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
}

.btn {
  border-radius: 8px;
  padding: 10px 20px;
  font-weight: 500;
}

.btn-block {
  width: 100%;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>