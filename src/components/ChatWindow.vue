<template>
  <div class="chat-window">
    <div class="card">
      <div class="card-header">
        <h5>与 {{ selectedUser.username }} 聊天</h5>
      </div>
      <div class="card-body messages-container">
        <div v-if="messages.length === 0" class="text-center py-5">
          <i class="fas fa-comments fa-3x text-muted mb-3"></i>
          <p class="text-muted">开始聊天吧！</p>
        </div>
        <div v-else class="messages-list">
          <div 
            v-for="message in messages" 
            :key="message.id"
            :class="['message', message.from_user.id === currentUserId ? 'message-own' : 'message-other']"
          >
            <div class="message-content">
              <div class="message-text">{{ message.message }}</div>
              <div class="message-meta">
                <small class="text-muted">
                  {{ new Date(message.created_at).toLocaleTimeString() }}
                </small>
                <span 
                  v-if="message.sentiment_label"
                  :class="['sentiment-badge', getSentimentClass(message.sentiment_label)]"
                  :title="`情感分数: ${message.sentiment_score}`"
                >
                  {{ getSentimentEmoji(message.sentiment_label) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer">
        <MessageInput @send-message="sendMessage" />
      </div>
    </div>
  </div>
</template>

<script>
import MessageInput from './MessageInput.vue'

export default {
  name: 'ChatWindow',
  components: {
    MessageInput
  },
  props: {
    currentUserId: {
      type: Number,
      required: true
    },
    selectedUser: {
      type: Object,
      required: true
    },
    channel: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      messages: [],
      pollTimer: null
    }
  },
  mounted() {
    this.loadMessages()
    this.pollTimer = setInterval(this.loadMessages, 3000)
  },
  beforeDestroy() {
    clearInterval(this.pollTimer)
  },
  methods: {
    async loadMessages() {
      try {
        const response = await this.$axios.get(`/get-messages/?channel=${this.channel.id}`)
        this.messages = response.data
      } catch (error) {
        console.error('加载消息失败:', error)
      }
    },
    
    async sendMessage(messageText) {
      try {
        const messageData = {
          message: messageText,
          from_user: this.currentUserId,
          to_user: this.selectedUser.id,
          channel: this.channel.id
        }
        
        const response = await this.$axios.post('/send-message/', messageData)
        this.messages.push(response.data)
        
        // 滚动到底部
        this.$nextTick(() => {
          const container = this.$el.querySelector('.messages-container')
          container.scrollTop = container.scrollHeight
        })
      } catch (error) {
        console.error('发送消息失败:', error)
        this.$bvToast.toast('发送消息失败', {
          title: '错误',
          variant: 'danger',
          solid: true
        })
      }
    },
    
    getSentimentClass(label) {
      const classMap = {
        positive: 'sentiment-positive',
        negative: 'sentiment-negative',
        neutral: 'sentiment-neutral'
      }
      return classMap[label] || 'sentiment-neutral'
    },
    
    getSentimentEmoji(label) {
      const emojiMap = {
        positive: '😊',
        negative: '😔',
        neutral: '😐'
      }
      return emojiMap[label] || '😐'
    }
  }
}
</script>

<style scoped>
.chat-window {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.messages-container {
  height: 400px;
  overflow-y: auto;
  padding: 15px;
}

.messages-list {
  display: flex;
  flex-direction: column;
}

.message {
  margin-bottom: 15px;
  display: flex;
}

.message-own {
  justify-content: flex-end;
}

.message-other {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 15px;
  position: relative;
}

.message-own .message-content {
  background-color: #007bff;
  color: white;
  border-bottom-right-radius: 5px;
}

.message-other .message-content {
  background-color: #f8f9fa;
  color: #333;
  border-bottom-left-radius: 5px;
}

.message-text {
  margin-bottom: 5px;
  word-wrap: break-word;
}

.message-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
}

.sentiment-badge {
  font-size: 1.2rem;
  margin-left: 5px;
}

.sentiment-positive {
  color: #28a745;
}

.sentiment-negative {
  color: #dc3545;
}

.sentiment-neutral {
  color: #6c757d;
}

.card-footer {
  background-color: #f8f9fa;
  border-top: 1px solid #dee2e6;
}
</style> 