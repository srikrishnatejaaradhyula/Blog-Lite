<template>
        <img :src="imageUrl" alt="" class="d-inline-block align-text-top rounded-circle" />
</template>

<script>
import { ref, onMounted } from 'vue'
export default {
    name: "GetProfilePic",
    props: {
        user_id: {
            type: Number,
            required: true
        }
    },
    setup(props) {
        const imageUrl = ref('')
        console.log(props.user_id)
        onMounted(async () => {
            const response2 = await fetch('http://127.0.0.1:5000/api/get_profile_img', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    id: props.user_id
                })
            })
            const blob = await response2.blob()
            const objectUrl = URL.createObjectURL(blob)
            imageUrl.value = objectUrl
        })
        return {
            imageUrl
        }
    }
}
</script>