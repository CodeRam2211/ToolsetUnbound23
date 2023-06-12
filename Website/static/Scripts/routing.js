



if(location.href == "http://127.0.0.1:5000/"){
    const login = document.querySelector(".in-btn")
    login.addEventListener("click", ()=>{
        location.replace("/login")
    })
}

if(location.href == "http://127.0.0.1:5000/dashboard"){
    const signout = document.querySelector(".lout")
    const logo = document.querySelector(".logo")
    const myFiles = document.querySelector("#files")
    console.log(myFiles)
    console.log(logo)
    signout.addEventListener("click", ()=>{
        console.log("Clicked")
        location.replace("/")
    })
    logo.addEventListener("click", ()=>{
        console.log("Clicked")
        location.reload()
    })

    myFiles.addEventListener("click", ()=>{
        console.log("Clicked")
        location.replace("/files")
    })
}
