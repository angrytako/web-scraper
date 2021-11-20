import { Toggler, CarDiv, CarParamsSelector} from "./Classes.js"
    let app2 = new Vue({
    el: '#app',
    data: {
        message: 'You loaded this page on ' + new Date().toLocaleString()
    },
    created: async function(){
        this.carsSearchParams = new CarParamsSelector();
        /*{nome:{value:null,op:"like"},prezzo:{value:4000,op:"<="},
    url:{value:null,op:null},imgUrl:{value:null,op:null},date:{value:null,op:null},
    euro:{value:4,op:">="},km:{value:140000,op:null},description:{value:null,op:null},
    creationDate:{value:null,op:null},expired:{value:false,op:"="},lastChecked:{value:null,op:null}}*/
        this.cars = await sendSearch(this.carsSearchParams.toDbObj(), this.cars);
        this.cars.sort((car1,car2) => car1.price - car2.price)
    },
    data: {
    cars:undefined,
    buttonStatus: "ByPrice",
    carsSearchParams:null,
    wantsNulls:{}

  },
  methods:{
    changeOrderElems,
    replaceWithInput,
    update,
    closeAlltabs,
    commit,
    reload,
    sendSearch
  }
    })
function toggleSpinner(){
    const spinner = document.querySelector("#spinner");
    if(spinner.style.display == "none") spinner.style.display="flex";
    else spinner.style.display = "none"
}

async function sendSearch(params, cars){
    toggleSpinner();
    const carsReq = await fetch("./getCars",
                            {
                                method:"POST",
                                headers:{"Content-Type":"application/json"},
                                body:JSON.stringify(params)
                            });
                            if(cars) {this.cars = await carsReq.json();
                                Object.keys(this.wantsNulls).forEach(key =>{
                                    console.log(this.wantsNulls[key])
                                    if(this.wantsNulls[key] == false)
                                    this.cars = this.cars.filter(
                                        car => car[key]
                                    )
                                })
                                changeOrderElems.bind(this)()  
                                changeOrderElems.bind(this)()    }
     else {
                                const res = await carsReq.json() 
                                return res;
                            } 
    toggleSpinner();
}
const carsToggled = new Map(); 

function changeOrderElems(e){
    if(this.buttonStatus=="ByPrice")
    {
        this.buttonStatus="ByRecency"
        this.cars.sort((car1,car2) => new Date(car2.creationDate).getTime() - new Date(car1.creationDate).getTime())
    }
    else if(this.buttonStatus=="ByRecency")
    {
        this.buttonStatus="ByPrice"
        this.cars.sort((car1,car2) => car1.price - car2.price)
    }
}
function replaceWithInput(e , car){
    let carDiv = carsToggled.get(car.url);
    let toggler;
    if(carDiv){
        toggler = carDiv[e.target.getAttribute("name")];
        if(toggler  && toggler.isBeingModified == false ){
            toggler.isBeingModified = true;
        }
        else{
            toggler = new Toggler([ e.target.nextElementSibling],[ e.target.previousElementSibling, e.target]);
            carDiv[e.target.getAttribute("name")] = toggler;
        }
        toggler.toggle();
        e.target.nextElementSibling.querySelector("input,textarea").focus();

    }
    else{
        carDiv = new CarDiv();
        toggler = new Toggler([ e.target.nextElementSibling],[ e.target.previousElementSibling, e.target]);
        carDiv[e.target.getAttribute("name")] = toggler;
        carsToggled.set(car.url,carDiv);
        toggler.toggle();
        e.target.nextElementSibling.querySelector("input,textarea").focus();
    }

}
function update(e,car){
    e.preventDefault();
    let carDiv = carsToggled.get(car.url);
    let toggler;
    if(carDiv){
        toggler = carDiv[e.target.getAttribute("name")];
        if(toggler  && toggler.isBeingModified == true ){
            toggler.isBeingModified = false;
        }
        else{
            toggler = new Toggler([ e.target.parentElement.previousElementSibling, e.target.parentElement.previousElementSibling.previousElementSibling],[e.target.parentElement],false);
            carDiv[e.target.getAttribute("name")] = toggler;
        }
        toggler.toggle();
    }
    else{
        carDiv = new CarDiv();
        toggler =  new Toggler([ e.target.parentElement.previousElementSibling, e.target.parentElement.previousElementSibling.previousElementSibling],[e.target.parentElement],false);
        carDiv[e.target.getAttribute("name")] = toggler;
        carsToggled.set(car.url,carDiv);
        toggler.toggle();
    }    
}

function closeAlltabs(e,car){
    const carDiv = carsToggled.get(car.url);
    if(carDiv) carDiv.toggleAllOff();
}

async function commit(e,car){
    toggleSpinner();
    const resp = await fetch("/update",
                            {
                                method:"POST",
                                headers:{"Content-Type":"application/json"},
                                body:JSON.stringify(car)
                            }
                            );
    const respMessage = await resp.text();
    toggleSpinner();
    console.log(respMessage);
}

async function reload(e, car){
    toggleSpinner();
    const resp = await fetch("/reload",
                            {
                                method:"POST",
                                headers:{"Content-Type":"application/json"},
                                body:JSON.stringify(car)
                            }
                            );
    const newCar = await resp.json();
    toggleSpinner();
    console.log(newCar);
    car.lastChecked = newCar.lastChecked;
    car.price = newCar.price;
    car.km = newCar.km;
    car.euro = newCar.euro;
    car.description = newCar.description;
    car.fuel = newCar.fuel;
}