<template>
    <div>
        <Nav />
        <div class="postbox container d-flex justify-content-evenly ">
            <div class="upload row  align-items-center">
                <div class="col-12 d-flex justify-content-center">
                    <!-- <img :src="imageUrl" v-if="imageUrl" height="300" width="300"> -->
                    <div >
                        <label class="custom-file-upload">
                            <input type="file" @input="onFileSelected">
                                <img :src="imageUrl" v-if="imageUrl" height="300" width="300">

                                <i class="bi bi-camera" v-else style="font-size: 10rem; color: #ced4da;"></i>
                        </label>
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
                    <button type="submit"  @click.prevent="SaveProfile" class="btn btn-success">
                        <i class="bi bi-rocket-takeoff"></i> Post
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Nav from './Nav.vue';
import VueJwtDecode from 'vue-jwt-decode'
export default {
    name: "Post",
    components: {
        Nav,
    },
    setup() {
        const imageUrl = ref(null);
        const file = ref(null);
        const title= ref(null);
        const caption = ref(null);
        const router = useRouter()


        const onFileSelected = (e) => {

            file.value = e.target.files[0];
            const reader = new FileReader();
            // reader.readAsDataURL(file.value)
            reader.onload = e => {
                imageUrl.value = e.target.result;
            };
            reader.readAsDataURL(file.value);
        }

        const token = localStorage.getItem('token')
        const user = VueJwtDecode.decode(token)
        const SaveProfile = async () => {
            // console.log("this id image", imageUrl.value)
            // console.log("this is username", username.value)
            // console.log("this is description", description.value)
            // console.log("this is user id", user.id)
            // console.log("this is file", file.value)


            // const file1 = fileInput.value.files[0]
            const reader = new FileReader()
            reader.readAsDataURL(file.value)
            reader.onload = async () => {
                const base64 = reader.result.split(',')[1]

                console.log("this is base64",base64)

                try {

                    const response = await fetch('http://127.0.0.1:5000/api/create_post', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'x-access-tokens': localStorage.getItem('token')
                        },
                        // body: formData
                        body: JSON.stringify({
                            image: base64,
                            title: title.value,
                            caption: caption.value,
                            user_id: user.id
                        })
                    })
                    console.log(response)
                    const data = await response.json()
                    console.log(data.id)
                    if (response.status === 200) {
                        alert("Successfully Posted ")
                        imageUrl.value = null
                        title.value = null
                        caption.value = null
                    }

                   
                    if (response.status === 400) {
                        throw new Error(`${alert(data.error)}`);
                    }
                }
                catch (error) {
                    console.log(error)
                }
            }

        }
        return {
            imageUrl,
            file,
            title,
            caption,
            onFileSelected,
            SaveProfile,
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