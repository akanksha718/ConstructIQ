import {
  BrainCircuit,
  ChartColumn,
  Cpu,
  Files,
  FolderTree,
  LayoutDashboard,
  Settings,
  Upload,
  Users,
  type LucideIcon,
} from "lucide-react";

export interface NavItem {
  title: string;
  href: string;
  icon: LucideIcon;
}

export interface NavGroup {
  title: string;
  items: NavItem[];
}

export const consoleNavigation: NavGroup[] = [
  {
    title: "General",
    items: [
      {
        title: "Dashboard",
        href: "/admin/dashboard",
        icon: LayoutDashboard,
      },
    ],
  },
  {
    title: "Knowledge Center",
    items: [
      {
        title: "Assets",
        href: "/admin/assets",
        icon: Files,
      },
      {
        title: "Upload",
        href: "/admin/upload",
        icon: Upload,
      },
      {
        title: "Collections",
        href: "/admin/knowledge/collections",
        icon: FolderTree,
      },
      {
        title: "Processing",
        href: "/console/knowledge/processing",
        icon: Cpu,
      },
    ],
  },
  {
    title: "AI",
    items: [
      {
        title: "Knowledge Test",
        href: "/console/ai",
        icon: BrainCircuit,
      },
    ],
  },
  {
    title: "Management",
    items: [
      {
        title: "Users",
        href: "/console/users",
        icon: Users,
      },
      {
        title: "Analytics",
        href: "/console/analytics",
        icon: ChartColumn,
      },
      {
        title: "Settings",
        href: "/console/settings",
        icon: Settings,
      },
    ],
  },
];