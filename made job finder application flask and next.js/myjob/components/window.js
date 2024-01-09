import dynamic from "next/dynamic";

const CustomMap = dynamic(()=> import('@components/CustomMap'),{
    ssr : false
})


export default CustomMap