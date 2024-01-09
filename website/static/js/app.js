// show and hide password
try {
    document.getElementById("show_passwords").addEventListener('click', () => 
    {
        document.querySelectorAll(".password_input").forEach((password_input) =>
        {
            password_input.type === "password" ? password_input.type = "text" : password_input.type = "password";
        });
    });
} catch (error) {/* pass */}

// display product picture preview
try
{
    document.getElementById('customFile').addEventListener('change', (event) => 
    {
        document.getElementById("product_picture_preview_div").style.padding = "2em 0";

        var selected_profile_picture;

        for (let i = 0; i < event.target.files.length; i++)
        {
            selected_profile_picture = event.target.files[i]

            if (selected_profile_picture.type.startsWith("image/"))
            {

                const read_file = new FileReader()
                read_file.readAsDataURL(selected_profile_picture)

                read_file.addEventListener('load', () =>
                {
                    document.getElementById('product_picture_preview_div').insertAdjacentHTML("beforeend", 
                        `<img class="product_picture_preview" src="${read_file.result}" alt="Selected Image">`
                    );
                });
            }
        }
    });
} catch (error) { /* pass */}

// display store profile picture preview
try
{
    document.getElementById('customFile').addEventListener('change', (event) => 
    {
        const selected_profile_picture = event.target.files[0]

        const read_file = new FileReader()
        read_file.readAsDataURL(selected_profile_picture)

        read_file.addEventListener('load', () =>
        {
            document.getElementById('profile_picture_preview_div').innerHTML = `<img id="profile_picture_preview" src="${read_file.result}" alt="Selected Image">`
        });
    })
} catch (error) { /* pass */}

// switch tabs on the store profile page
try
{
    switch_tab(0)
} catch (error) {/* pass */}

document.addEventListener("click", (event) => 
{
    const clicked_element = event.target;

    // listen for changing of tabs
    if (clicked_element.className.includes("nav_bar_title"))
    {
        clicked_element.style.backgroundColor = '#193053';
        clicked_element.style.color = '#e3e1e3';
        
        switch_tab(parseInt(clicked_element.dataset.tabindex));
    }

    else if (clicked_element.className === "next_pic")
        next_picture(clicked_element)

    else if (clicked_element.className === "prev_pic")
        prev_picture(clicked_element)
});

// display and remove the contents of the list elements
function switch_tab(idx = -1)
{
    // change style of the tab title to potray current tab
    document.querySelectorAll(".nav_bar_title").forEach((button) =>
    {
        if (button.dataset.tabindex == idx)
        {
            button.style.color = "#e3e1e3";
            button.style.backgroundColor = "#193053";
        }
        else
        {
            button.style.color = "#404940";
            button.style.backgroundColor = "#e3e1e3";
        }
    })

    // switch the tab
    const all_tabs = document.getElementById('nav_tabs').querySelectorAll("li");

    for (let i = 0; i < all_tabs.length; i++)
    {
        if (i != idx)
            all_tabs[i].style.display = "none";
        else
            all_tabs[i].style.display = "flex";
    }
}

// move to the next image in the slideshow of product_pictures
function next_picture(particular_product)
{
    // change style of the tab title to potray current tab
    const particular_each_pic_div = particular_product.parentElement.querySelector(".product_pictures_slideshow_div").querySelectorAll(".carousel-item");

    for (let i = 0; i < particular_each_pic_div.length; i++)
    {
        if (particular_each_pic_div[i].classList.contains("active"))
        {
            particular_each_pic_div[i].classList.remove("active");

            if (i == particular_each_pic_div.length-1)
                particular_each_pic_div[0].classList.add("active")
            else
                particular_each_pic_div[i + 1].classList.add("active")
            break;
        }
    }
}

// move to the previous image in the slideshow of product_pictures
function prev_picture(particular_product)
{
    // change style of the tab title to potray current tab
    const particular_each_pic_div = particular_product.parentElement.querySelector(".product_pictures_slideshow_div").querySelectorAll(".carousel-item");

    for (let i = 0; i < particular_each_pic_div.length; i++)
    {
        if (particular_each_pic_div[i].classList.contains("active"))
        {
            particular_each_pic_div[i].classList.remove("active");

            if (i == 0)
                particular_each_pic_div[particular_each_pic_div.length - 1].classList.add("active")
            else
                particular_each_pic_div[i - 1].classList.add("active")
            break;
        }
    }
}
