<template>
    <div>
        <button class="btn " @click="toggleLike" :style="{ color: liked ? 'blue' : 'gray' }">
            <h4><i class="bi bi-hand-thumbs-up-fill"></i></h4>
            <!-- {{ liked ? 'Liked' : 'Like' }} -->
        </button>
        <span>{{ count.value }} likes</span>
    </div>
</template>
  
<script>
import { ref, onMounted, watch, reactive } from 'vue'


export default {
    name: 'LikeButton',
    props: ['postId', 'userId'],
    setup(props) {
        const liked = ref('')
        // const count = ref()
        const count = reactive({ value: 0 })

        const postId = props.postId
         // Fetch the data and update count.value when it's available
        fetch('http://127.0.0.1:5000/api/like_count', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    postId: postId,
                })
            })
                .then(response => response.json())
                .then(data => {
                    count.value = data.count
                    console.log("count", count.value)
                })

        onMounted(async () => {
            const response = await fetch('http://127.0.0.1:5000/api/liked', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    postId: props.postId,
                    userId: props.userId,
                })
            })
            const data = response.json()
            console.log(data)
            if (data.liked == 0) {
                liked.value = false
            }
            else {
                liked.value = true
            }

            

        })



        // watchEffect(async () => {
        //     // Define props.postId as a dependency
        //     const postId = props.postId

        //     // Fetch the data and update count.value when it's available
        //     await fetch('http://127.0.0.1:5000/api/like_count', {
        //         method: 'POST',
        //         headers: {
        //             'Content-Type': 'application/json',
        //             'x-access-tokens': localStorage.getItem('token')
        //         },
        //         body: JSON.stringify({
        //             postId: postId,
        //         })
        //     })
        //         .then(response => response.json())
        //         .then(data => {
        //             count.value = data.count
        //             console.log("count", count.value)
        //         })
           
        // })

        const toggleLike = async () => {
            liked.value = !liked.value

            const response3 = await fetch('http://127.0.0.1:5000/api/like', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    postId: props.postId,
                    userId: props.userId,
                    liked: liked.value
                })
            })
            const data3 = response3.json()
            console.log(data3)
            if (liked.value == true) {
                count.value += 1
            }
            else {
                count.value -= 1
            }
        }

        return {
            liked,
            count,
            toggleLike
        }
    }
}

</script>
  