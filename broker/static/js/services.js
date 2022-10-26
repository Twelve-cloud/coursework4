const orderBtns = document.querySelectorAll('.btn-order');

orderBtns.forEach(btn => {
  btn.addEventListener('click', e => {
    const priceTd = e.target.parentElement.previousElementSibling;
    const username = document.getElementById('broker_name').textContent;
    
    const data = {
      username: username,
      company: priceTd.previousElementSibling.previousElementSibling.textContent,
      type: priceTd.previousElementSibling.textContent,
      price: priceTd.textContent
    }

    order(data);
  });
});


async function order(data) {
    const response = await fetch('/orders', {
        method: "PUT",
        header: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
}
