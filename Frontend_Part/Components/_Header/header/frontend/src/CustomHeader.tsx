import React from 'react';
import Logo from './static/check-circle.svg'; 
import { Client as Styletron } from "styletron-engine-atomic"
import { Provider as StyletronProvider } from "styletron-react"// Replace with the path to your logo
import {
  // ComponentProps,
  withStreamlitConnection,
  StreamlitComponentBase,
  // Streamlit,
} from "streamlit-component-lib"

const engine = new Styletron()

interface State {
  /**
   * The value specified by the user via the UI. If the user didn't touch this
   * widget's UI, the default value is used.
   */
  selectedIndex: number
}

class CustomHeader extends StreamlitComponentBase<State> {
  
  public constructor(props: any) {
    super(props)
    this.state = { selectedIndex: 0 }
  }  

  public render = (): React.ReactNode => {
    return (
      <StyletronProvider value={engine}>
        <Header />
      </StyletronProvider>
    )
  }

}



function Header() {
  return (
    <div id ="lolik" className="w-screen h-screen flex justify-between items-center p-6 shadow-sm bg-white max-w-full">
      <div>
        <img src={Logo} alt="Logo" className="mr-6 h-2rem" />
        <nav className="flex">
          <a href="/review" className="mx-3 text-lg text-gray-600 hover:text-gray-900">Review</a>
          <a href="/help" className="mx-3 text-lg text-gray-600 hover:text-gray-900">Help</a>
          <a href="/authors" className="mx-3 text-lg text-gray-600 hover:text-gray-900">Authors</a>
        </nav>
      </div>
      <div>
        <button className="mr-4 bg-indigo-500 text-white py-2 px-4 rounded">RateMe</button>
        <a href="/login" className="mx-3 text-lg text-gray-600 hover:text-gray-900">Login</a>
        <a href="/register" className="mx-3 text-lg text-gray-600 hover:text-gray-900">Register</a>
      </div>
    </div>
  );
}

export default withStreamlitConnection(CustomHeader);
