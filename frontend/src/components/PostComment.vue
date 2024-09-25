<template>
    <div>
        <Nav />
        <div class="container d-flex justify-content-center" style="width: 100%">
            <div class="card" style="width: 70%">
                <div class="card-header">
                    <div class="d-flex justify-content-between">
                        <div class="d-flex">
                            <!-- <img src="src\assets\Person-icon.png" alt="" width="30" height="30"
                                class="d-inline-block align-text-top rounded-circle" /> -->

                            <GetPorfilePic width="30" height="30" :user_id="id"></GetPorfilePic>

                            <a href="/login" class="align-middle text-decoration-none" style="color: black">
                                {{ username }}</a>
                            <p class="text-end align-top ms-2 fw-light" style="display: inline; font-size: 12px">
                                {{ created_at }} days ago
                            </p>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="container-fluid">
                        <div class="row">
                            <div class="col-12 col-md-6 col-lg-6">

                                <GetPostImage width="350" height="350" :post_id="ids"></GetPostImage>


                                <div class="col">
                                <h5 class="card-title">{{ title }}</h5>
                                <p class="card-text">{{ description }}</p>
                            </div>
                            </div>
                            <div class="col-12 col-md-6 col-lg-6 align-items-end" style="height: 400px; overflow-y: auto">

                                <div v-for="c in comments.comm" class="card my-2" style="width: 100%">
                                    <div class="card-header">
                                    
                                        <GetPorfilePic width="30" height="30" :user_id="c.user_id"></GetPorfilePic>
                                        
                                        <h6 style="display:inline">{{c.username}}</h6>
                                    </div>
                                    <div class="card-body p-0 m-0">
                                        <p class="text-end">{{c.comment}}</p>
                                        <!-- <p class="text-start" v-else>hello</p> -->
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-footer ">
                    <div class="form-floating form-group d-flex" style="width:100%;">
                        <input type="text" class="form-control" v-model="comment" id="floatingInput" placeholder=" "
                            required />
                        <label for="floatingInput">Comment</label>
                        <button class="btn btn-success btn-sm" @click.prevent="PostComment()" style="width:30%;">
                            <i class="bi bi-chat"></i> Comment
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import GetPostImage from "./GetPostImage.vue";
import {reactive, ref, computed, onMounted } from "vue";
import { useRoute,useRouter } from "vue-router";
import Nav from "./Nav.vue";
import VueJwtDecode from 'vue-jwt-decode'
import GetPorfilePic from "./GetPorfilePic.vue";


export default {
    name: "PostComment",
    components: {
        Nav,
        GetPostImage,
        GetPorfilePic
    },
    setup() {
        const comment = ref("");
        const comments = reactive({
            comm: []
        })
        const username = ref("");
        const id = ref("");
        const title = ref("");
        const description = ref("");
        const created_at = ref("");

        const route = useRoute()
        const router = useRouter()

        const ids = computed(() => route.params.id);
        console.log("this is comments id", ids.value)
        const token = localStorage.getItem('token')
        const user = VueJwtDecode.decode(token)

        const PostComment = async () => {
            const response = await fetch("http://127.0.0.1:5000/api/comment", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    "post_id": ids.value,
                    "comment": comment.value,
                    "user_id": user.id
                })
            })
            const data = await response.json()
            console.log("this is comments", data)
            if (response.ok) {
                alert("commented")
                comment.value = ""
                router.go(0)
            }
        }

        onMounted(async() => {
            const response2 = await fetch("http://127.0.0.1:5000/api/get_comments", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    "post_id": ids.value,
                })

            })
            const data = await response2.json()
            console.log("this is comments", data)
            comments.comm = data

            const response3 = await fetch("http://127.0.0.1:5000/api/get_post_comment_data", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    "post_id": ids.value,
                })

            })
            const data2 = await response3.json()
            console.log("this is comments", data2)
            username.value = data2.username
            id.value = data2.id
            title.value = data2.title
            description.value = data2.description
            created_at.value = data2.created_at

        })


        return {
            comment,
            PostComment,
            ids,
            comments,
            username,
            id,
            title,
            description,
            created_at

        };

    },
};

</script>