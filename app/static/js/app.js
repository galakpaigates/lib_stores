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
        if (event.target.files[0].type.startsWith("image/"))
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
        
        if (selected_profile_picture.type.startsWith("image/"))
        {
            const read_file = new FileReader()
            read_file.readAsDataURL(selected_profile_picture)

            read_file.addEventListener('load', () =>
            {
                document.getElementById('profile_picture_preview_div').innerHTML = 
				`
					<img id="profile_picture_preview" src="${read_file.result}" alt="Selected Image">
				`
            });
        }
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

    if (clicked_element.id !== "search_results_div" && clicked_element.id !== "search_input" && clicked_element.id !== "search_btn")
        document.getElementById("search_results_div").style.display = "none";

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

    else if (clicked_element.id === "clear_search_input_div")
        document.getElementById("search_input").value = "";
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

document.addEventListener("DOMContentLoaded", () => 
{
    // listen for input on the search field and make an ajax request to the search endpoint to query the database for matching information
    $("#search_input").on("input", (event) =>
    {
        const search_query = event.target.value;

        // remove the search_results_div and do nothing else if the input field is blank
        if (search_query.length <= 0)
        {
            document.getElementById("search_results_div").style.display = "none";
            return;
        }

        // send request
        $.ajax({
            url: "/search/",
            method: "POST",
            data: JSON.stringify({
                query_value: search_query
            }),
            dataType: 'json',
            contentType: 'application/json',
            success: ((_res) =>
            {
                display_search_results(_res);
            }),
            error: ((_res) =>
            {
                console.error(_res)
            })
        });
    });

    navbar_height = document.getElementById("navbar").offsetHeight;
    document.querySelector("main").style.marginTop = navbar_height + "px";

    try
    {
        flash_btn = document.getElementById("display_flashed_messages_modal_btn")
        flash_btn.click()
        flash_btn.remove();
    }
    catch { /* pass */ }

    try
    {
        // check if the product description is more that 800 characters and make the div scrollable
        if (document.getElementById("particular_product_description_h5").textContent.length > 800)
            document.getElementById("product_information_and_quantity_form_div").style.position = "relative";

        // check if the product name is more than 35 characters and the product name is more than 400 characters and make the div scrollable
        else if (document.getElementById("store_name_div").children[0].textContent.length > 30 && document.getElementById("particular_product_description_h5").textContent.length > 400 && window.innerWidth < 1800)
            document.getElementById("product_information_and_quantity_form_div").style.position = "relative";

        // check if the product name is more than 40 characters then make the div scrollable
        else if (document.getElementById("store_name_div").children[0].textContent.length > 40 && window.innerWidth < 1800)
            document.getElementById("product_information_and_quantity_form_div").style.position = "relative";
    }
    catch { /* pass */ }
});

function display_search_results(results)
{
    const search_results_div = document.getElementById("search_results_div");

    if (results.length <= 0)
    {
        search_results_div.innerHTML = "<h3>No match found!</h3>";
        return;
    }

    search_results_div.innerHTML = "";
    search_results_div.style.display = "flex";
	search_results_div.style.zIndex = "100000";

    for (let i = 0; i < results.length; i++)
    {
        search_results_div.insertAdjacentHTML('beforeend',
        `
            <a href="/products/${results[i].id}+${results[i].store_id}">
                <div class="each_search_result_div">
                    <img class="each_search_result_img" src="data:image/png;base64,${results[i].picture}" alt="${results[i].name}">
                    <div class="each_search_result_info_div">
                        <span class="search_result_name_span">
                            ${results[i].name}
                        </span>
                        <span class="search_result_price_available_quantity_span">
                            $${results[i].price} &bull; ${results[i].quantity} in stock
                        </span>
                    </div>
                </div>
            </a>
        `);
    }
}

document.getElementById("search_form").addEventListener("submit", (event) => 
{
    event.preventDefault();
});

