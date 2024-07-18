const city_input = document.querySelector('.form__city .city--input');  // ���� � ������ ������
const hint = document.querySelectorAll('.hint');  // ���� ������ ������� ������
const city_submit = document.querySelector('.form__city .city--submit'); // ������ "������"

city_input.addEventListener('input', () => {
    const city_input_value = city_input.value.toLowerCase();
    fetch('/cities/')
        .then(response => response.json())
        .then(data => {
            const cities = data['city']
                .filter(city => city.name.toLowerCase().includes(city_input_value))
                .slice(0, 5);
            let hint_content = '';  // ��������� ���������
            for(let city of cities){
                hint_content += `<li class="hint__item"><p class="item__name">${city.name}</p></li>`;
            }
            hint[0].innerHTML = hint_content;

        })
        .catch(error => console.error('Error:', error));
});

for(let hint_item of hint){
    hint_item.addEventListener('click', (ev) => {
        if(ev.target.classList.contains('item__name')){  // ���� ����� �� ��������� ������
            city_input.value = ev.target.textContent;
            city_submit.click();
        }
    })
}
