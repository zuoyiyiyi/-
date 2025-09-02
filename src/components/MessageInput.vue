<template>
  <div class="message-input">
    <form @submit.prevent="sendMessage">
      <div class="input-group">
        <input
          v-model="message"
          type="text"
          class="form-control"
          placeholder="输入消息..."
        >
        <div class="input-group-append">
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="!message.trim()"
          >
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'MessageInput',
  data() {
    return {
      message: ''
    }
  },
  methods: {
    sendMessage() {
      if (this.message.trim()) {
        this.$emit('send-message', this.message.trim())
        this.message = ''
      }
    }
  }
}
</script>

<style scoped>
.message-input {
  padding: 10px;
}

.input-group {
  border-radius: 20px;
  overflow: hidden;
}

.form-control {
  border: none;
  padding: 10px 15px;
}

.form-control:focus {
  box-shadow: none;
  border-color: #007bff;
}

.btn {
  border: none;
  padding: 10px 15px;
  border-radius: 0 20px 20px 0;
}

.btn:disabled {
  opacity: 0.6;
}
</style>