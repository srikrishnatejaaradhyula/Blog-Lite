<template>
    <div>
        <Nav />
        <div class="postbox container d-flex justify-content-evenly ">
            <div class="upload row  align-items-center">
                <div class="col-12 d-flex justify-content-center">
                    <!-- <img :src="imageUrl" v-if="imageUrl" height="300" width="300"> -->
                    <div >
                        <!-- <label class="custom-file-upload">
                            <input type="file" @input="onFileSelected">
                                <img :src="imageUrl" v-if="imageUrl" height="300" width="300">

                                <i class="bi bi-camera" v-else style="font-size: 10rem; color: #ced4da;"></i>
                        </label> -->
                        <GetPostImage width="250" height="250" :post_id="ids" ></GetPostImage>
                    </div>
                </div>

                <div class="col-12">
                    <div class="form-floating mb-3">
                            <input type="text" class="form-control" v-model="title" id="floatingInput" placeholder=" "
                                required />
                            <label for="floatingInput">Title</label>
                        </div>
                    <div class="form-floating">
                        <textarea class="form-control" v-model="caption" placeholder="Leave a comment here" id="floatingTextarea"></textarea>
                        <label for="floatingTextarea">Caption</label>
                    </div>
                </div>

                <div class="col-12 d-flex justify-content-end">
                    <button type="submit"  @click.prevent="UpdatePost" class="btn btn-success">
                        <i class="bi bi-rocket-takeoff"></i> Update
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref,computed,onMounted } from 'vue';
import {useRoute} from 'vue-router';
import Nav from './Nav.vue';
import VueJwtDecode from 'vue-jwt-decode'
import GetPostImage from './GetPostImage.vue'
export default {
    name: "Post",
    components: {
        Nav,
        GetPostImage
    },
    setup() {
        const title= ref('');
        const caption = ref('');
        const route = useRoute()
        const ids = computed(() => route.params.id);

        const token = localStorage.getItem('token')
        const user = VueJwtDecode.decode(token)

        onMounted(async() => {
            const response2 = await fetch('http://127.0.0.1:5000/api/get_post_comment_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    post_id: ids.value
                })
            })
            const data2 = await response2.json()
            console.log(data2)
            title.value = data2.title
            caption.value = data2.description
        })


        const UpdatePost = async () => {     

                try {

                    const response = await fetch('http://127.0.0.1:5000/api/update_post', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'x-access-tokens': localStorage.getItem('token')
                        },
                        // body: formData
                        body: JSON.stringify({
        
                            title: title.value,
                            caption: caption.value,
                            user_id: user.id,
                            post_id : ids.value
                        })
                    })
                    console.log(response)
                    const data = await response.json()
                    console.log(data.id)
                    if (response.status === 200) {
                        alert("Successfully updated")
                    }

                   
                    if (response.status === 400) {
                        throw new Error(`${alert(data.error)}`);
                    }
                }
                catch (error) {
                    console.log(error)
                }

        }
        return {
            title,
            caption,
            UpdatePost,
            ids
        }
    }
}
</script>

<style>
.form-floating input[type="text"],
.form-floating input[type="email"],
.form-floating input[type="password"],
.form-floating textarea {
    border: none;
    border-radius: 0;
    border-bottom: 1px solid #ced4da;
}

input[type="file"] {
    display: none;
}

.postbox {
    width: 75%;
    /* height: 100vh; */
}

.upload {
    height: 85vh;
    background: rgba(230, 253, 253, 0.279);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
}
</style>