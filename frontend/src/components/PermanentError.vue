<template>
    <div class="alert alert-danger" role="alert">
        {{ message }}
    </div>
</template>

<script>
export default {
  props: {
    message: { required: true, type: String }
  }
}
</script>