

// var width = 1000;
// var height = 500;
// var randomY = [];
// var svg = d3.select("body")
//   .append("svg")
//   .attr("width", width)
//   .attr("height", height);

// // Функция, имитирующая получение данных с сервера
// $('.btn').on('click', updateChart(randomY.slice(-5)));

// // function update_arr(num) {
// //   randomY.push(num)
// //   let chart_random = (randomY.slice(-5))
//   // updateChart(chart_random)}

// randomY = [100, 50, 23, 20, 257];
// function fetchData(num) {
//   randomY.push(num)
//   let chart_random = (randomY.slice(-20))
//   updateChart(chart_random)
// }


// // Функция для обновления графика с использованием полученных данных
// function updateChart(data) {
//   svg.selectAll("path").remove();
//   // svg.selectAll("ellipse").remove();

//   var lineFunction = d3.line()
//     .x(function (d, i) { return i * (width / (data.length - 1)); })
//     .y(function (d) { return d; })
//     ; // Заменяем curveLinear на curveBasis для плавной анимации

//   svg.append("path")
//     .datum(data) // Добавляем .datum(), чтобы D3 могло анимировать плавно
//     .attr("class", "line")
//     .attr("d", lineFunction)
//     .attr("stroke", "red")
//     .attr("stroke-width", 3)
//     .attr("fill", "none")
//     // .transition() // Добавляем анимацию
//     // .duration(5000) // Продолжительность анимации в миллисекундах
//     // .ease(d3.easeLinear) // Тип анимации
//     // .attr("d", lineFunction(data)); // Изменяем путь для плавной анимации
// }
// updateChart(randomY)

// Создаем SVG элемент
var svg = d3.select("body").append("svg")
    .attr("width", "800%")
    .attr("height", 500);
    // .attr("top: 500px");

// Инициализируем начальные данные
var data = [480];
var t = 0;

function generateData(num) {
  console.log(data[data.length - 1], num, 0)
  t = ((500 - num) - data[data.length - 1]) / 100
  console.log(t, 1)

  if (data.length > 100 * 100) {
      data.shift();
    }
}

// Определяем функцию для обновления графика
function update() {
    // Добавляем новую точку данных
    var t1 = (data[data.length - 1] + t)
    console.log(t1, 2)
    data.push(t1)
    // data.push(500)
    // Обновляем xScale
    xScale.domain([0, data.length - 1]);

    // Обновляем линию
    svg.select("path")
        .attr("d", line(data))
        .attr("transform", null)
      .transition()
        .duration(0)
        .ease(d3.easeLinear)
        .attr("transform", "translate(" + xScale(-1) + ",0)") // Сдвигаем влево на один пиксель

    // Удаляем излишние данные
}

// Определяем xScale
var xScale = d3.scaleLinear()
    .domain([0, 100])
    .range([0, window.innerWidth]);

// Определяем line
var line = d3.line()
    .x(function(d, i) { return xScale(i); })
    .y(function(d) { return d; });

// Добавляем линию
svg.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 2);

// Запускаем обновление каждую секунду
setInterval(update, 10);
