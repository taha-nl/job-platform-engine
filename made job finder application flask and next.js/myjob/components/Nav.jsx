"use client"
import React from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { useState,useEffect } from 'react'
const Nav = () => {
  return (
    <nav className='flex-between w-full mb-16 pt-3'>
      <Link href="/" className='flex gap-2 flex-center'>
      <Image src="/images/logo.svg" 
      alt='Job finder'
      width={50}
      height={50}
      />
      <p className='logo_text'>Job finder</p>
      
      </Link>
    </nav>
  )
}

export default Nav