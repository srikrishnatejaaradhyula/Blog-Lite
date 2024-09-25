<template>
    <button class="btn btn-outline-gray" @click="toggleFollow" :style="{ color : following ? 'green' : 'red' }">
        <i class="bi bi-person-add"></i>  {{ following ? 'Following' : 'Follow' }}
    </button>
</template>
  
<script>
import { ref,onMounted } from 'vue'
import VueJwtDecode from 'vue-jwt-decode'

export default {
    props: ['followerId', 'followedId'],
    setup(props) {
        const following = ref('')

        // axios.get(`/follow?followerId=${props.followerId}&followedId=${props.followedId}`)
        //     .then(response => {
        //         following.value = response.data.following
        //     })
        
        const token = localStorage.getItem('token')
        const user = VueJwtDecode.decode(token)    

        console.log("hi this is follower: ",props.followerId)
        console.log("hi this is followed",props.followedId)

        onMounted(async () => {
            const response = await fetch('http://127.0.0.1:5000/api/following',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    followerId: props.followerId,
                    followedId: props.followedId,
                })
            })
            const data = await response.json()
            console.log("hi this is data",data.following)
            if (data.following == 0) {
                following.value = false
            }
            else {
                following.value = true
            }
            // following.value = data.following
        })


        const toggleFollow = () => {
            following.value = !following.value

            fetch('http://127.0.0.1:5000/api/follow', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-access-tokens': localStorage.getItem('token')
            },
            body: JSON.stringify({
                followerId: props.followerId,
                followedId: props.followedId,
                following: following.value
            })
        })
        }

        return {
            following,
            toggleFollow
        }
    }
}
</script>
  