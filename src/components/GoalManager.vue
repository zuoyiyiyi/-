<template>
  <div class="goal-manager">
    <div class="container">
      <h2 class="mb-4">目标管理</h2>
      
      <!-- 创建新目标 -->
      <div class="card mb-4">
        <div class="card-header">
          <h5>创建新目标</h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="createGoal">
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label>目标标题</label>
                  <input 
                    v-model="newGoal.title" 
                    type="text" 
                    class="form-control" 
                    placeholder="例如：每天阅读"
                    required
                  >
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label>频率</label>
                  <select v-model="newGoal.frequency" class="form-control">
                    <option value="daily">每日</option>
                    <option value="weekly">每周</option>
                    <option value="monthly">每月</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="form-group">
              <label>目标描述</label>
              <textarea 
                v-model="newGoal.description" 
                class="form-control" 
                rows="3"
                placeholder="详细描述你的目标..."
              ></textarea>
            </div>
            <button type="submit" class="btn btn-primary">创建目标</button>
          </form>
        </div>
      </div>
      
      <!-- 目标列表 -->
      <div class="card">
        <div class="card-header">
          <h5>我的目标</h5>
        </div>
        <div class="card-body">
          <div v-if="goals.length === 0" class="text-center py-4">
            <p class="text-muted">还没有创建任何目标</p>
          </div>
          <div v-else class="row">
            <div v-for="goal in goals" :key="goal.id" class="col-md-6 mb-3">
              <div class="card h-100">
                <div class="card-body">
                  <h6 class="card-title">{{ goal.title }}</h6>
                  <p class="card-text text-muted">{{ goal.description || '暂无描述' }}</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="badge badge-primary">{{ getFrequencyText(goal.frequency) }}</span>
                    <div>
                      <button 
                        @click="editGoal(goal)" 
                        class="btn btn-sm btn-outline-primary mr-2"
                      >
                        编辑
                      </button>
                      <button 
                        @click="deleteGoal(goal.id)" 
                        class="btn btn-sm btn-outline-danger"
                      >
                        删除
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
    </div>
  </div>
</template>

<script>
export default {
  name: 'GoalManager',
  props: {
    userId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      goals: [],
      batchReminders: [],
      newGoal: {
        title: '',
        description: '',
        frequency: 'daily',
        target_count: 1,
        is_active: true
      }
    }
  },
  mounted() {
    this.loadGoals()
    this.loadBatchReminders()
  },
  methods: {
    async loadGoals() {
      try {
        const response = await this.$axios.get(`/goals/?user_id=${this.userId}`)
        this.goals = response.data
      } catch (error) {
        console.error('加载目标失败:', error)
        this.$bvToast.toast('加载目标失败', {
          title: '错误',
          variant: 'danger',
          solid: true
        })
      }
    },
    async loadBatchReminders() {
      try {
        const response = await this.$axios.get(`/batch-reminders/`, { params: { user_id: this.userId } })
        this.batchReminders = response.data
      } catch (error) {
        console.error('AI提示获取失败:', error)
        this.batchReminders = []
      }
    },
    getReminderByGoalId(goalId) {
      return this.batchReminders.find(r => r.goal_id === goalId)
    },
    async createGoal() {
      try {
        const goalData = {
          ...this.newGoal,
          user_id: this.userId
        }
        const response = await this.$axios.post('/goals/', goalData)
        this.goals.push(response.data)
        // 重置表单
        this.newGoal = {
          title: '',
          description: '',
          frequency: 'daily',
          target_count: 1,
          is_active: true
        }
        this.$bvToast.toast('目标创建成功', {
          title: '成功',
          variant: 'success',
          solid: true
        })
        // 新增：创建目标后刷新AI提示
        this.loadBatchReminders()
      } catch (error) {
        console.error('创建目标失败:', error)
        this.$bvToast.toast('创建目标失败', {
          title: '错误',
          variant: 'danger',
          solid: true
        })
      }
    },
    // 新增：外部可调用，打卡后刷新AI提示
    refreshReminders() {
      this.loadBatchReminders()
    },
    async editGoal(goal) {
      // 这里可以实现编辑功能
      console.log('编辑目标:', goal)
    },
    
    async deleteGoal(goalId) {
      if (confirm('确定要删除这个目标吗？')) {
        try {
          await this.$axios.delete(`/goals/${goalId}/`)
          this.goals = this.goals.filter(goal => goal.id !== goalId)
          
          this.$bvToast.toast('目标删除成功', {
            title: '成功',
            variant: 'success',
            solid: true
          })
        } catch (error) {
          console.error('删除目标失败:', error)
          this.$bvToast.toast('删除目标失败', {
            title: '错误',
            variant: 'danger',
            solid: true
          })
        }
      }
    },
    
    getFrequencyText(frequency) {
      const frequencyMap = {
        daily: '每日',
        weekly: '每周',
        monthly: '每月'
      }
      return frequencyMap[frequency] || frequency
    }
  }
}
</script>

<style scoped>
.goal-manager {
  padding: 20px;
}

.card {
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.form-group {
  margin-bottom: 1rem;
}

.badge {
  font-size: 0.8rem;
}

.ai-reminder {
  font-size: 14px;
  color: #888;
  margin-top: 4px;
}
.ai-reminder.checked {
  color: #42b983;
}
</style> 