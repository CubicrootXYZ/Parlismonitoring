<template>
    <!-- item -->
    <div class="col-xl-3 col-md-4 mb-3">
        <div class="card border-left-primary shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-s font-weight-bold text-primary text-uppercase mb-1">
                            {{ title }}
                        </div>
                        <div class="mini-card-value">
                            {{ value }}
                        </div>
                    </div>

                    <div class="col-auto">
                        <i :class="[icon, 'fas', 'fa-2x', 'text-primary']"></i>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'MiniCard',
  props: {
    title: { required: true, type: String},
    value: { required: true, type: String},
    icon: { required: true, type: String},
  }
}
</script>