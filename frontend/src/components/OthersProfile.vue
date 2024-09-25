<template>
    <div>
        <Nav />
        <div class="container-fluid">
            <div class="row">
                <div class="col-12 col-md-4 col-lg-4 d-flex justify-content-center">
                    <GetPorfilepic  width="150" height="150" :user_id="ids"></GetPorfilepic>
                </div>
                <div div class="col-12 col-md-6 col-lg-6">
                    <div class="row">
                        <div class="col">
                            <h4 style="display: inline">{{ username }}</h4>
                            <!-- <router-link to="/edit-profile" class="btn">Edit Profile</router-link> -->
                            <h6>{{ description }}</h6>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-4 col-md-4 col-lg-4">
                            <h4>Posts <br>{{ posts }} </h4>
                        </div>
                        <div class="col-4 col-md-4 col-lg-4">
                            <h4>Followers <br>{{ followers }} </h4>
                        </div>
                        <div class="col-4 col-md-4 col-lg-4">
                            <h4>Following<br> {{following }}</h4>
                        </div>
                    </div>
                </div>
            </div>
            <!-- </div>

        <div class="container-fluid"> -->
            <div class="row">
                <div class="card_style col-lg-4 col-sm-4 col-12 my-5 d-flex justify-content-evenly" v-for="p in post.Posts" :key="p.id">
                    <!-- post -->

                    <div class="card" style="">
                        <div class="card-header">
                            <div class="d-flex justify-content-between">
                                <div class="d-flex">
                                    <!-- <img src="src\assets\Person-icon.png" alt="" width="30" height="30"
                                        class="d-inline-block align-text-top rounded-circle" /> -->
                                    <GetPorfilepic  width="30" height="30" :user_id="ids"></GetPorfilepic>

                                    <a href="/login" class="align-middle text-decoration-none" style="color: black">
                                        {{ username }}</a>
                                    <p class="text-end align-top ms-2 fw-light" style="display: inline; font-size: 12px">
                                        {{ p.created_at }} days ago
                                    </p>
                                </div>
                                
                            </div>
                        </div>
                        
                        <GetPostImage :post_id="p.id" height="300"></GetPostImage>

                        <div class="card-body">
                            <h5 class="card-title">{{ p.title }}</h5>
                            <p class="card-text">{{ p.description }}</p>
                        </div>
                    </div>
                </div>
            </div>


        </div>
    </div>
</template>

<script>
import Nav from './Nav.vue';
import GetPorfilepic from './GetPorfilePic.vue'
// import VueJwtDecode from 'vue-jwt-decode'
import { reactive,computed,onMounted,ref } from 'vue'
import { useRoute } from 'vue-router'
import LikeButton from './LikeButton.vue'
import GetPostImage from './GetPostImage.vue'



export default {
    name: "OthersProfile",
    components: {
        Nav,
        GetPorfilepic,
        LikeButton,
        GetPostImage
    },
    setup() {
        const route = useRoute()
        const username = ref('')
        const description = ref('')
        const posts = ref('')
        const followers = ref('')
        const following = ref('')
        const post = reactive({
            Posts: []
        });
        const ids = computed(() => route.params.id);
        const token = localStorage.getItem('token')
        // const user = VueJwtDecode.decode(token)
        onMounted(async () => {
            const response = await fetch("http://127.0.0.1:5000/api/profile_posts", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    user_id: ids.value
                })
            });
            // console.log("this is user id", user.id)
            const data = await response.json()
            post.Posts = data
            console.log(post.Posts)

            const response1 = await fetch("http://127.0.0.1:5000/api/get_profile", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    user_id: ids.value
                })
            });
            const data1 = await response1.json()
            username.value = data1.username
            description.value = data1.description
            console.log(data1)

            
            const response2 = await fetch("http://127.0.0.1:5000/api/other_data", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    user_id: ids.value
                })
            })
            const data2 = await response2.json()
            console.log(data2)
            posts.value = data2.post
            followers.value = data2.followers
            following.value = data2.following

        });
        console.log("this is ID :", ids.value)
        return {
            post,
            ids,
            username,
            description,
            posts,
            followers,
            following
        }
    }


}
</script>

<style scoped>
.card {
    background: rgba(230, 253, 253, 0.226);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    width: 50vh;
}

.card:hover {
    width: 52vh;
}
</style>