import React from "react";
import { Navbar, NavbarBrand } from "reactstrap";

export default class NavBar extends React.Component {
  render() {
    return (
      <div>
        <Navbar color="dark" light expand="md">
          <NavbarBrand href="/">PenherApp</NavbarBrand>
        </Navbar>
      </div>
    );
  }
}
