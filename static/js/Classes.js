export class Toggler{
    constructor(toBeSetVisible, toBeHidden,isBeingModified = true){
        this.isBeingModified =isBeingModified;
        this.toBeSetVisible = toBeSetVisible;
        this.toBeHidden = toBeHidden;
    }
    toggle(){
        this.toBeSetVisible.forEach(element => {
            element.style.display = "inline-block";
        });
        this.toBeHidden.forEach(element => {
            element.style.display = "none";
        });
        let sup = this.toBeSetVisible;
        this.toBeSetVisible = this.toBeHidden
        this.toBeHidden = sup;
    }
}
export class CarDiv{
    constructor(name=null,imgUrl=null ,price=null,euro=null,km=null,description=null){
        this.name = name
        this.imgUrl = imgUrl
        this.price = price
        this.euro = euro
        this.km = km
        this.description = description
    }
    toggleAllOff(){
        if(this.name && this.name.isBeingModified)
            this.name.toggle();
        if(this.imgUrl && this.imgUrl.isBeingModified)
            this.imgUrl.toggle();
        if(this.price && this.price.isBeingModified)
            this.price.toggle();
        if(this.euro && this.euro.isBeingModified)
            this.euro.toggle();
        if(this.km && this.km.isBeingModified)
            this.km.toggle();
        if(this.description && this.description.isBeingModified)
            this.description.toggle();
    }
}

export class CarParamsSelector {
    constructor(nome={value:null,op:"like"},prezzo={value:4000,op:"<="},
    url={value:null,op:null},imgUrl={value:null,op:null},date={value:null,op:null},
    euro={value:4,op:">="},km={value:140000,op:null},description={value:null,op:null},
    creationDate={value:null,op:null},expired={value:false,op:"="},lastChecked={value:null,op:null}){
        this.nome = nome
        this.prezzo = prezzo
        this.imgUrl = imgUrl
        this.euro = euro
        this.km = km
        this.description = description
        this.creationDate = creationDate
        this.expired = expired
        this.lastChecked = lastChecked

    }
    toDbObj(){
        let nome={};
        if(this.nome.value) {
            nome.value = "%"+this.nome.value+"%";
            nome.op = this.nome.op}
        else nome = null;
        return {
            nome,
            prezzo:this.prezzo,
            imgUrl:this.imgUrl,
            euro:this.euro,
            km:this.km,
            description:this.description,
            creationDate:this.creationDate,
            expired:this.expired,
            lastChecked:this.lastChecked

        }
    }
}