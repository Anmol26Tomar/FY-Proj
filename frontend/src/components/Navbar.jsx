import { Link, useNavigate } from 'react-router-dom'
import { Moon, Sun, BookOpen, LogOut, User, LogIn, UserPlus } from 'lucide-react'

const Navbar = ({ darkMode, toggleTheme }) => {
  const navigate = useNavigate();

  // Simple auth check via localStorage
  const userStr = localStorage.getItem('user');
  const user = userStr ? JSON.parse(userStr) : null;

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          <div className="nav-logo-icon">
            <BookOpen size={20} />
          </div>
          <span className="nav-logo-text">
            Scholar-Agent
          </span>
        </Link>
        
        <div className="nav-actions">
          <button 
            onClick={toggleTheme}
            className="btn-icon"
            aria-label="Toggle Theme"
          >
            {darkMode ? <Sun size={20} /> : <Moon size={20} />}
          </button>
          
          {user ? (
             <>
               <div className="btn-text" style={{display: 'flex', alignItems: 'center', gap: '0.4rem'}}>
                 <User size={18} /> <span className="nav-logo-text hide-on-mobile" style={{fontSize: '0.875rem'}}>{user.name}</span>
               </div>
               <button onClick={handleLogout} className="btn-primary" style={{display: 'flex', alignItems: 'center', gap: '0.4rem', backgroundColor: '#ef4444', boxShadow: 'none'}}>
                 <LogOut size={16} /> <span className="hide-on-mobile">Logout</span>
               </button>
             </>
          ) : (
             <>
               <Link to="/login" className="btn-text" style={{display: 'flex', alignItems: 'center', gap: '0.4rem'}}>
                 <LogIn size={18} className="mobile-icon-only" /> <span className="hide-on-mobile">Login</span>
               </Link>
               <Link to="/login" className="btn-primary" style={{display: 'flex', alignItems: 'center', gap: '0.4rem'}}>
                 <UserPlus size={18} className="mobile-icon-only" /> <span className="hide-on-mobile">Sign up</span>
               </Link>
             </>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
