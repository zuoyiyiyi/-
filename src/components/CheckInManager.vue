<template>
  <div class="checkin-manager">
    <div class="container">
      <h2 class="mb-4">打卡管理</h2>
      
      <!-- 打卡统计 -->
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="card text-center">
            <div class="card-body">
              <h4 class="text-primary">{{ stats.total_checkins }}</h4>
              <p class="card-text">总打卡次数</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-center">
            <div class="card-body">
              <h4 class="text-success">{{ stats.consecutive_days }}</h4>
              <p class="card-text">连续打卡天数</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-center">
            <div class="card-body">
              <h4 :class="stats.today_checkin ? 'text-success' : 'text-warning'">
                {{ stats.today_checkin ? '已打卡' : '未打卡' }}
              </h4>
              <p class="card-text">今日状态</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 最近7天打卡情况 -->
      <div class="card mb-4">
        <div class="card-header">
          <h5>最近7天打卡情况</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div v-for="(day, index) in stats.recent_checkins" :key="index" class="col">
              <div class="text-center">
                <div 
                  :class="day.checked ? 'checkin-day checked' : 'checkin-day unchecked'"
                  :title="day.date"
                >
                  {{ new Date(day.date).getDate() }}
                </div>
                <small class="text-muted">{{ new Date(day.date).getMonth() + 1 }}/{{ new Date(day.date).getDate() }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 打卡操作 -->
      <div class="card mb-4">
        <div class="card-header">
          <h5>今日打卡</h5>
        </div>
        <div class="card-body">
          <div v-if="goals.length === 0" class="text-center py-4">
            <p class="text-muted">请先创建目标</p>
          </div>
          <div v-else>
            <div v-for="goal in goals" :key="goal.id" class="mb-3">
              <div class="card">
                <div class="card-body">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h6 class="card-title">{{ goal.title }}</h6>
                      <p class="card-text text-muted">{{ goal.description }}</p>
                    </div>
                    <div>
                      <button 
                        @click="checkIn(goal)" 
                        class="btn btn-success"
                        :disabled="isCheckedIn(goal.id)"
                      >
                        {{ isCheckedIn(goal.id) ? '已打卡' : '打卡' }}
                      </button>
                    </div>
                  </div>
                  <!-- AI提示语展示 -->
                  <div v-if="getReminderByGoalId(goal.id)" class="ai-reminder mt-2" :class="{ checked: getReminderByGoalId(goal.id).checked }">
                    <i class="fa fa-magic mr-1" aria-hidden="true"></i>
                    {{ getReminderByGoalId(goal.id).ai_reminder }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- AI提醒消息 -->
      <div v-if="aiMessage" class="card">
        <div class="card-header">
          <h5>AI提醒</h5>
        </div>
        <div class="card-body">
          <div class="alert alert-info">
            <i class="fas fa-robot mr-2"></i>
            {{ aiMessage }}
          </div>
        </div>
      </div>
      
      <!-- 打卡记录 -->
      <div class="card">
        <div class="card-header">
          <h5>打卡记录</h5>
        </div>
        <div class="card-body">
          <div v-if="checkins.length === 0" class="text-center py-4">
            <p class="text-muted">还没有打卡记录</p>
          </div>
          <div v-else>
            <div v-for="checkin in checkins" :key="checkin.id" class="checkin-record">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h6>{{ checkin.goal.title }}</h6>
                  <p class="text-muted mb-0">
                    {{ new Date(checkin.check_in_date).toLocaleDateString() }}
                    <span v-if="checkin.notes" class="ml-2">- {{ checkin.notes }}</span>
                  </p>
                </div>
                <div class="text-right">
                  <span v-if="checkin.mood_score" class="badge badge-info">
                    心情: {{ checkin.mood_score }}/10
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 打卡模态框 -->
    <b-modal v-model="showCheckInModal" title="打卡" @ok="submitCheckIn">
      <div class="form-group">
        <label>心情评分 (1-10)</label>
        <input 
          v-model="checkInForm.mood_score" 
          type="number" 
          class="form-control" 
          min="1" 
          max="10"
        >
      </div>
      <div class="form-group">
        <label>备注</label>
        <textarea 
          v-model="checkInForm.notes" 
          class="form-control" 
          rows="3"
          placeholder="今天感觉如何？有什么想说的吗？"
        ></textarea>
      </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'CheckInManager',
  props: {
    userId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      goals: [],
      checkins: [],
      stats: {
        total_checkins: 0,
        consecutive_days: 0,
        today_checkin: false,
        recent_checkins: []
      },
      aiMessage: '',
      batchReminders: [],
      showCheckInModal: false,
      checkInForm: {
        goal_id: null,
        mood_score: 7,
        notes: ''
      }
    }
  },
  mounted() {
    this.loadData()
    this.loadBatchReminders()
  },
  methods: {
    async loadData() {
      await Promise.all([
        this.loadGoals(),
        this.loadCheckins(),
        this.loadStats()
      ])
    },
    
    async loadGoals() {
      try {
        const response = await this.$axios.get(`/goals/?user_id=${this.userId}`)
        this.goals = response.data
      } catch (error) {
        console.error('加载目标失败:', error)
      }
    },
    
    async loadCheckins() {
      try {
        const response = await this.$axios.get(`/checkins/?user_id=${this.userId}`)
        this.checkins = response.data
      } catch (error) {
        console.error('加载打卡记录失败:', error)
      }
    },
    
    async loadStats() {
      try {
        const response = await this.$axios.get(`/checkin-stats/?user_id=${this.userId}`)
        this.stats = response.data
      } catch (error) {
        console.error('加载统计信息失败:', error)
      }
    },
    
    async loadBatchReminders() {
      try {
        const response = await this.$axios.get('/batch-reminders/', { params: { user_id: this.userId } })
        this.batchReminders = response.data
      } catch (error) {
        console.error('AI提示获取失败:', error)
        this.batchReminders = []
      }
    },
    
    checkIn(goal) {
      this.checkInForm.goal_id = goal.id
      this.showCheckInModal = true
    },
    
    async submitCheckIn() {
      try {
        const today = new Date().toISOString().split('T')[0]
        const checkInData = {
          user_id: this.userId,
          goal_id: this.checkInForm.goal_id,
          mood_score: Number(this.checkInForm.mood_score),
          notes: this.checkInForm.notes,
          check_in_date: today
        }
        
        const response = await this.$axios.post('/checkins/', checkInData)
        
        // 显示AI激励消息
        if (response.data.ai_message) {
          this.aiMessage = response.data.ai_message
        }
        
        // 重新加载数据
        await this.loadData()
        
        // 重置表单
        this.checkInForm = {
          goal_id: null,
          mood_score: 7,
          notes: ''
        }
        
        this.$bvToast.toast('打卡成功！', {
          title: '成功',
          variant: 'success',
          solid: true
        })
        // 新增：打卡后通知父组件刷新目标AI提示
        this.$emit('refresh-goal-reminders')
        // 新增：打卡后自动刷新AI提示
        this.loadBatchReminders()
      } catch (error) {
        console.error('打卡失败:', error)
        this.$bvToast.toast('打卡失败', {
          title: '错误',
          variant: 'danger',
          solid: true
        })
      }
    },
    
    getReminderByGoalId(goalId) {
      return this.batchReminders.find(r => r.goal_id === goalId)
    },
    
    isCheckedIn(goalId) {
      const today = new Date().toISOString().split('T')[0]
      return this.checkins.some(checkin => 
        checkin.goal.id === goalId && 
        checkin.check_in_date === today
      )
    }
  }
}
</script>

<style scoped>
.checkin-manager {
  padding: 20px;
}

.card {
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.checkin-day {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 5px;
  font-weight: bold;
}

.checkin-day.checked {
  background-color: #28a745;
  color: white;
}

.checkin-day.unchecked {
  background-color: #f8f9fa;
  color: #6c757d;
  border: 2px solid #dee2e6;
}

.checkin-record {
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.checkin-record:last-child {
  border-bottom: none;
}

.alert {
  border-radius: 10px;
}

.ai-reminder {
  font-size: 0.8em;
  color: #6c757d;
}

.ai-reminder.checked {
  color: #28a745;
}
</style> 