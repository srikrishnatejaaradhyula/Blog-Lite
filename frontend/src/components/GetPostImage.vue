<template>
    <img :src="imageUrl" class="card-img-top"  alt=""  />
</template>

<script>
import { ref, onMounted } from 'vue'
export default {
name: "GetPostImage",
props: {
    post_id: {
        type: Number,
        required: true
    }
},
setup(props) {
    const imageUrl = ref('')
    console.log("this props from getpostimg ",props.post_id)
    onMounted(async () => {
        const response = await fetch('http://127.0.0.1:5000/api/post_img', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-access-tokens': localStorage.getItem('token')
            },
            body: JSON.stringify({
                post_id: props.post_id
            })
        })
        const blob = await response.blob()
        const objectUrl = URL.createObjectURL(blob)
        imageUrl.value = objectUrl
        console.log("this is image url",imageUrl.value)
    })
    return {
        imageUrl
    }
}
}
</script>