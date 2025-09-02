<template>
  <div class="user-list">
    <div class="card">
      <div class="card-header">
        <h5>用户列表</h5>
      </div>
      <div class="card-body">
        <div v-if="users.length === 0" class="text-center py-4">
          <p class="text-muted">没有其他用户</p>
        </div>
        <div v-else>
          <div 
            v-for="user in users" 
            :key="user.id"
            class="user-item"
            @click="$emit('select-user', user)"
          >
            <div class="d-flex align-items-center">
              <div class="user-avatar">
                <i class="fas fa-user"></i>
              </div>
              <div class="user-info">
                <h6 class="mb-0">{{ user.username }}</h6>
                <small class="text-muted">在线</small>
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
  name: 'UserList',
  props: {
    users: {
      type: Array,
      default: () => []
    },
    currentUserId: {
      type: Number,
      required: true
    }
  }
}
</script>

<style scoped>
.user-list {
  height: 100%;
}

.user-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-item:hover {
  background-color: #f8f9fa;
}

.user-item:last-child {
  border-bottom: none;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #007bff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.user-info {
  flex: 1;
}
</style> 